import logging
from typing import Optional
from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories.subscription_plan_repo import SubscriptionPlanRepository
from app.models.subscription_plan import SubscriptionPlan, PlanStatus
from app.models.audit_log import AuditLog
from app.schemas.subscription_plan import SubscriptionPlanCreate, SubscriptionPlanUpdate

logger = logging.getLogger(__name__)

# Valid state machine transitions
ALLOWED_TRANSITIONS = {
    PlanStatus.DRAFT: [PlanStatus.ACTIVE],
    PlanStatus.ACTIVE: [PlanStatus.INACTIVE, PlanStatus.ARCHIVED],
    PlanStatus.INACTIVE: [PlanStatus.ACTIVE],
    PlanStatus.ARCHIVED: [], # Final state
}

class SubscriptionPlanService:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.repo = SubscriptionPlanRepository(session)

    async def _write_audit_log(
        self,
        action: str,
        entity_id: str,
        actor_id: Optional[str],
        old_values: Optional[dict] = None,
        new_values: Optional[dict] = None,
        ip_address: Optional[str] = None,
    ):
        audit = AuditLog(
            actor_type="admin",
            actor_id=actor_id or "system",
            action=action,
            entity="subscription_plan",
            entity_id=entity_id,
            old_values=old_values,
            new_values=new_values,
            ip_address=ip_address,
        )
        self.session.add(audit)

    async def create_plan(
        self, data: SubscriptionPlanCreate, admin_id: str = "admin", ip_address: Optional[str] = None
    ) -> SubscriptionPlan:
        async with self.session.begin():
            if await self.repo.get_by_name(data.name):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Plan with name '{data.name}' already exists."
                )

            slug = self.repo.generate_slug(data.name)
            if await self.repo.get_by_slug(slug):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Generated slug '{slug}' already exists."
                )

            plan = SubscriptionPlan(
                name=data.name.strip(),
                slug=slug,
                description=data.description,
                price=data.price,
                currency=data.currency,
                duration_days=data.duration_days,
                max_api_keys=data.max_api_keys,
                max_services=data.max_services,
                max_monthly_invoices=data.max_monthly_invoices,
                status=PlanStatus.DRAFT,
                display_order=data.display_order,
                created_by=admin_id,
                updated_by=admin_id,
            )
            await self.repo.create(plan)
            
            # Serialize for audit log
            new_payload = data.model_dump(mode="json")
            new_payload["slug"] = slug
            new_payload["status"] = PlanStatus.DRAFT.value
            
            await self._write_audit_log(
                action="PLAN_CREATED",
                entity_id=str(plan.id),
                actor_id=admin_id,
                new_values=new_payload,
                ip_address=ip_address,
            )
            return plan

    async def update_plan(
        self,
        plan_id: str,
        data: SubscriptionPlanUpdate,
        admin_id: str = "admin",
        ip_address: Optional[str] = None,
    ) -> SubscriptionPlan:
        async with self.session.begin():
            plan = await self.repo.get_by_id(plan_id)
            if not plan:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Plan not found")

            if plan.status == PlanStatus.ARCHIVED:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST, detail="Archived plans cannot be updated."
                )

            old_values = {
                "name": plan.name,
                "price": str(plan.price),
                "duration_days": plan.duration_days,
                "display_order": plan.display_order,
            }

            update_dict = data.model_dump(exclude_unset=True)
            if "name" in update_dict and update_dict["name"] != plan.name:
                if await self.repo.get_by_name(update_dict["name"]):
                    raise HTTPException(status_code=400, detail="Plan name already in use.")
                new_slug = self.repo.generate_slug(update_dict["name"])
                if await self.repo.get_by_slug(new_slug):
                    raise HTTPException(status_code=400, detail="Generated slug already exists.")
                plan.name = update_dict["name"]
                plan.slug = new_slug

            for field, val in update_dict.items():
                if field != "name" and hasattr(plan, field):
                    setattr(plan, field, val)

            plan.updated_by = admin_id

            await self._write_audit_log(
                action="PLAN_UPDATED",
                entity_id=str(plan.id),
                actor_id=admin_id,
                old_values=old_values,
                new_values=data.model_dump(mode="json", exclude_unset=True),
                ip_address=ip_address,
            )
            return plan

    async def transition_status(
        self,
        plan_id: str,
        target_status: PlanStatus,
        admin_id: str = "admin",
        ip_address: Optional[str] = None,
    ) -> SubscriptionPlan:
        async with self.session.begin():
            plan = await self.repo.get_by_id(plan_id)
            if not plan:
                raise HTTPException(status_code=404, detail="Plan not found.")

            if target_status not in ALLOWED_TRANSITIONS.get(plan.status, []):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Invalid transition from {plan.status.value} to {target_status.value}.",
                )

            action_map = {
                PlanStatus.ACTIVE: "PLAN_PUBLISHED" if plan.status == PlanStatus.DRAFT else "PLAN_ACTIVATED",
                PlanStatus.INACTIVE: "PLAN_DISABLED",
                PlanStatus.ARCHIVED: "PLAN_ARCHIVED",
            }
            
            old_status = plan.status.value
            plan.status = target_status
            plan.updated_by = admin_id

            await self._write_audit_log(
                action=action_map.get(target_status, "PLAN_STATUS_CHANGED"),
                entity_id=str(plan.id),
                actor_id=admin_id,
                old_values={"status": old_status},
                new_values={"status": target_status.value},
                ip_address=ip_address,
            )
            return plan