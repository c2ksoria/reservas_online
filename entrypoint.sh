#!/bin/sh

echo "⏳ Esperando a la base de datos en $DB_HOST:$DB_PORT..."

# Esperar a que la base de datos esté lista
while ! nc -z "$POSTGRES_HOST" "$POSTGRES_PORT"; do
  sleep 1
done

echo "✅ Base de datos disponible. Ejecutando migraciones..."

# Forzar makemigrations por app
poetry run python reservas/manage.py makemigrations app
poetry run python reservas/manage.py makemigrations members
poetry run python reservas/manage.py makemigrations
poetry run python reservas/manage.py migrate

# Importar datos iniciales (solo si no fue hecho antes)
if [ ! -f "/app/.initialized" ]; then
  echo "📥 Importando datos de configuración inicial..."

  # # Datos base necesarios para funcionamiento (setup)
  
  poetry run python reservas/manage.py loaddata reservas/reservas/fixtures/ReservationOrigin.json
  poetry run python reservas/manage.py loaddata reservas/reservas/fixtures/ReservationStatus.json
  poetry run python reservas/manage.py loaddata reservas/reservas/fixtures/PaymentsType.json

  # # Datos de ejemplo (demo/test)
  poetry run python reservas/manage.py loaddata reservas/reservas/fixtures/Data/Commercial.json
  poetry run python reservas/manage.py loaddata reservas/reservas/fixtures/Data/Property.json
  poetry run python reservas/manage.py loaddata reservas/reservas/fixtures/Data/Reservation.json
  poetry run python reservas/manage.py loaddata reservas/reservas/fixtures/Data/Payments.json

  echo "✅ Datos iniciales cargados correctamente."
  touch /app/.initialized
else
  echo "ℹ️  Datos ya fueron cargados anteriormente, omitiendo importación."
fi

# Crear superusuario automáticamente si no existe (opcional)
if [ "$DJANGO_SUPERUSER_USERNAME" ]; then
  echo "🔍 Verificando si el superusuario '$DJANGO_SUPERUSER_USERNAME' ya existe..."

  poetry run python reservas/manage.py shell << END
from django.contrib.auth import get_user_model
User = get_user_model()
username = "$DJANGO_SUPERUSER_USERNAME"

if not User.objects.filter(username=username).exists():
    User.objects.create_superuser(
        username=username,
        email="$DJANGO_SUPERUSER_EMAIL",
        password="$DJANGO_SUPERUSER_PASSWORD"
    )
    print("✅ Superusuario creado exitosamente: " + username)
else:
    print("ℹ️  El superusuario ya existe: " + username)
END
fi

echo "🚀 Iniciando servidor Django..."
exec poetry run python reservas/manage.py runserver 0.0.0.0:8000
