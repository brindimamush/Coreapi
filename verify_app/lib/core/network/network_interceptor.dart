import 'package:dio/dio.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../config/env.dart';
import '../storage/secure_storage.dart';

class NetworkInterceptor extends Interceptor {
  final Ref ref;

  NetworkInterceptor(this.ref);

  @override
  void onRequest(RequestOptions options, RequestInterceptorHandler handler) async {
    // Inject backend API keys or future JWT tokens here
    options.headers['X-Internal-API-Key'] = Env.internalApiKey;
    options.headers['Content-Type'] = 'application/json';
    
    // Example: Fetching a theoretical auth token from storage
    // final token = await ref.read(storageServiceProvider).readData('auth_token');
    // if (token != null) {
    //   options.headers['Authorization'] = 'Bearer $token';
    // }

    super.onRequest(options, handler);
  }
}