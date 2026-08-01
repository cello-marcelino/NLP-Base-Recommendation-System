FROM node:18-alpine

WORKDIR /app

COPY package*.json ./
RUN npm install

COPY . .

EXPOSE 5173

# Jalankan dalam mode development (agar sama seperti testing lokal)
# Atau jika ingin production, bisa ganti CMD dengan build + serve
CMD ["npm", "run", "dev", "--", "--host"]
