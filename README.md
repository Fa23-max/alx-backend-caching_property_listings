# ALX Backend Caching Property Listings

Django project with Redis caching for property listings management.

## Features

- **Property Management**: CRUD operations for property listings
- **Redis Caching**: Multi-level caching strategy with page-level and low-level caching
- **Cache Invalidation**: Automatic cache invalidation using Django signals
- **Cache Metrics**: Redis cache hit/miss ratio analysis
- **PostgreSQL Database**: Robust database backend
- **Docker Support**: Containerized PostgreSQL and Redis services

## Setup Instructions

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Start Docker Services
```bash
docker-compose up -d
```

### 3. Run Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### 4. Create Superuser (Optional)
```bash
python manage.py createsuperuser
```

### 5. Run Development Server
```bash
python manage.py runserver
```

## API Endpoints

- `GET /properties/` - List all properties (cached for 15 minutes)

## Caching Strategy

1. **Page-level caching**: Property list view cached for 15 minutes
2. **Low-level caching**: Property queryset cached for 1 hour
3. **Cache invalidation**: Automatic cache clearing on property create/update/delete
4. **Cache metrics**: Real-time Redis performance monitoring

## Docker Services

- **PostgreSQL**: Available at `localhost:5432`
- **Redis**: Available at `localhost:6379`