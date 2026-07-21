import 'package:dio/dio.dart';
import 'package:flutter/foundation.dart';

class ErrorInterceptor extends Interceptor {
  @override
  void onError(DioException err, ErrorInterceptorHandler handler) {
    final statusCode = err.response?.statusCode;
    final path = err.requestOptions.path;

    debugPrint('API Error [$statusCode] at $path: ${err.message}');
    
    if (statusCode == 401 || statusCode == 403) {
      // Handle unauthorized access globally (e.g., clear secure storage, redirect to login)
      debugPrint('Unauthorized or Forbidden access detected.');
    } else if (statusCode == 422) {
      // Matches the FastAPI Validation Error response[cite: 1]
      debugPrint('Validation Error: ${err.response?.data}');
    }

    super.onError(err, handler);
  }
}