import re
from typing import Optional, Sequence
from sqlalchemy import select, func, or_
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.subscription_plan import SubscriptionPlan, PlanStatus

class SubscriptionPlanRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    @staticmethod
    def generate_slug(name: str) -> str:
        slug = re.sub(r"[^\w\s-]", "", name.lower())
        return re.sub(r"[-\s]+", "-", slug).strip("-")

    async def get_by_id(self, plan_id: str) -> Optional[SubscriptionPlan]:
        result = await self.session.execute(
            select(SubscriptionPlan).where(SubscriptionPlan.id == plan_id)
        )
        return result.scalar_one_or_none()

    async def get_by_name(self, name: str) -> Optional[SubscriptionPlan]:
        result = await self.session.execute(
            select(SubscriptionPlan).where(SubscriptionPlan.name.ilike(name.strip()))
        )
        return result.scalar_one_or_none()

    async def get_by_slug(self, slug: str) -> Optional[SubscriptionPlan]:
        result = await self.session.execute(
            select(SubscriptionPlan).where(SubscriptionPlan.slug == slug)
        )
        return result.scalar_one_or_none()

    async def create(self, plan: SubscriptionPlan) -> SubscriptionPlan:
        self.session.add(plan)
        await self.session.flush()
        return plan

    async def get_active_plans(self) -> Sequence[SubscriptionPlan]:
        result = await self.session.execute(
            select(SubscriptionPlan)
            .where(SubscriptionPlan.status == PlanStatus.ACTIVE)
            .order_by(SubscriptionPlan.display_order.asc(), SubscriptionPlan.created_at.desc())
        )
        return result.scalars().all()

    async def get_all_paginated(
        self, skip: int = 0, limit: int = 20, search: str = "", status: Optional[PlanStatus] = None
    ) -> tuple[Sequence[SubscriptionPlan], int]:
        query = select(SubscriptionPlan)
        if search:
            search_term = f"%{search}%"
            query = query.where(
                or_(
                    SubscriptionPlan.name.ilike(search_term),
                    SubscriptionPlan.slug.ilike(search_term),
                )
            )
        if status:
            query = query.where(SubscriptionPlan.status == status)

        count_query = select(func.count()).select_from(query.subquery())
        total = await self.session.scalar(count_query) or 0

        query = query.order_by(SubscriptionPlan.display_order.asc(), SubscriptionPlan.created_at.desc()).offset(skip).limit(limit)
        result = await self.session.execute(query)
        return result.scalars().all(), total

    async def get_stats(self) -> dict:
        total = await self.session.scalar(select(func.count()).select_from(SubscriptionPlan)) or 0
        active = await self.session.scalar(
            select(func.count()).select_from(SubscriptionPlan).where(SubscriptionPlan.status == PlanStatus.ACTIVE)
        ) or 0
        drafts = await self.session.scalar(
            select(func.count()).select_from(SubscriptionPlan).where(SubscriptionPlan.status == PlanStatus.DRAFT)
        ) or 0
        archived = await self.session.scalar(
            select(func.count()).select_from(SubscriptionPlan).where(SubscriptionPlan.status == PlanStatus.ARCHIVED)
        ) or 0

        return {
            "totalPlans": total,
            "activePlans": active,
            "draftPlans": drafts,
            "archivedPlans": archived,
        }