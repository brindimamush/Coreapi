class Env {
  // Use 10.0.2.2 for Android Emulator to access localhost:8000
  static const String apiBaseUrl = String.fromEnvironment(
    'API_BASE_URL',
    defaultValue: 'http://10.0.2.2:8000/api/v1',
  );

  static const String internalApiKey = String.fromEnvironment(
    'INTERNAL_API_KEY',
    defaultValue: 'dev-internal-key',
  );
}