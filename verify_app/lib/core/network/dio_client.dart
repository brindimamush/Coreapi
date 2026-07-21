import 'package:dio/dio.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../config/env.dart';
import 'error_interceptor.dart';
import 'network_interceptor.dart';

final dioProvider = Provider<Dio>((ref) {
  final dio = Dio(
    BaseOptions(
      baseUrl: Env.apiBaseUrl,
      connectTimeout: const Duration(seconds: 15),
      receiveTimeout: const Duration(seconds: 15),
    ),
  );

  dio.interceptors.addAll([
    NetworkInterceptor(ref),
    ErrorInterceptor(),
    if (const bool.fromEnvironment('dart.vm.product') == false)
      LogInterceptor(requestBody: true, responseBody: true),
  ]);

  return dio;
});