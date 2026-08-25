# Configuration

Aturan pemisahan configuration dari application logic. Berlaku saat menambah environment variable atau config baru.

---

Configuration harus dipisahkan dari application logic: `.env`, `config/`, environment variables.

```env
# Application
APP_NAME=MyApp
APP_ENV=development
APP_DEBUG=true
APP_URL=http://localhost:8000

# Database
DB_HOST=localhost
DB_PORT=3306
DB_DATABASE=myapp
DB_USERNAME=root
DB_PASSWORD=

# Authentication
JWT_SECRET=your-secret-key

# External API
API_URL=https://api.example.com
API_KEY=your-api-key

# AI / LLM
AI_PROVIDER=openai
AI_API_KEY=your-ai-api-key
AI_MODEL=your-model-name

# Cache
CACHE_ENABLED=true
REDIS_HOST=localhost
REDIS_PORT=6379
```

Rules:
- Jangan hardcode secret
- Jangan commit password
- Jangan commit API key
- Jangan hardcode environment-specific configuration
- Gunakan `.env.example` untuk mendokumentasikan required variables

Lihat juga `rules/security.md`.
