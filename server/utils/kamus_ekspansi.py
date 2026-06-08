# __all__ = ["KAMUS_EKSPANSI", "ekspansi_query"] 

KAMUS_EKSPANSI = {

    # ── AI & DEEP LEARNING ─────────────────────────────────────────────
    "deep learning": [
        "neural network", "cnn", "rnn", "lstm", "gru", "transformer",
        "bert", "gpt", "autoencoder", "gan", "feedforward",
        "backpropagation", "jaringan saraf tiruan", "jst",
        "deep neural network", "dnn"
    ],
    "machine learning": [
        "pembelajaran mesin", "svm", "support vector machine",
        "random forest", "decision tree", "naive bayes", "knn",
        "k-nearest neighbor", "gradient boosting", "xgboost",
        "regresi", "prediksi", "supervised learning",
        "unsupervised learning", "reinforcement learning"
    ],
    "kecerdasan buatan": [
        "artificial intelligence", "ai", "sistem pakar", "expert system",
        "logika fuzzy", "fuzzy logic", "agen cerdas", "intelligent agent"
    ],
    "transfer learning": [
        "fine tuning", "pretrained model", "feature extraction",
        "domain adaptation", "model reuse"
    ],
    "generative ai": [
        "large language model", "llm", "diffusion model",
        "stable diffusion", "text to image", "prompt engineering",
        "rag", "retrieval augmented generation"
    ],
    "optimasi model": [
        "hyperparameter tuning", "learning rate", "dropout",
        "regularisasi", "batch normalization", "early stopping",
        "overfitting", "underfitting", "cross validation"
    ],

    # ── COMPUTER VISION ────────────────────────────────────────────────
    "klasifikasi gambar": [
        "image classification", "image recognition", "citra digital",
        "computer vision", "resnet", "vgg", "efficientnet",
        "inception", "mobilenet"
    ],
    "deteksi objek": [
        "object detection", "yolo", "rcnn", "faster rcnn", "ssd",
        "feature pyramid network", "bounding box", "anchor box",
        "nms", "non maximum suppression"
    ],
    "segmentasi": [
        "image segmentation", "semantic segmentation",
        "instance segmentation", "unet", "mask rcnn",
        "panoptic segmentation", "pixel classification"
    ],
    "pengolahan citra": [
        "image processing", "opencv", "preprocessing citra",
        "augmentasi data", "thresholding", "edge detection",
        "morfologi citra", "histogram equalization", "noise reduction"
    ],
    "pengenalan wajah": [
        "face recognition", "face detection", "facial landmark",
        "facenet", "deepface", "arcface", "liveness detection", "biometrik"
    ],
    "ocr": [
        "optical character recognition", "text detection",
        "document analysis", "tesseract", "crnn",
        "handwriting recognition", "document digitization"
    ],

    # ── NLP & TEXT ─────────────────────────────────────────────────────
    "pemrosesan bahasa alami": [
        "natural language processing", "nlp", "text mining",
        "text analysis", "corpus", "tokenisasi", "tokenization",
        "stemming", "lemmatization", "pos tagging"
    ],
    "analisis sentimen": [
        "sentiment analysis", "opinion mining", "klasifikasi teks",
        "text classification", "polaritas", "emosi teks",
        "ulasan", "review analysis"
    ],
    "information retrieval": [
        "pencarian informasi", "search engine", "temu balik informasi",
        "tf idf", "bm25", "inverted index", "query expansion",
        "relevance ranking"
    ],
    "word embedding": [
        "word2vec", "fasttext", "glove", "embedding",
        "representasi vektor", "semantic similarity",
        "cosine similarity", "dense retrieval"
    ],
    "chatbot": [
        "conversational ai", "dialog system", "intent recognition",
        "entity extraction", "ner", "named entity recognition",
        "slot filling", "rasa", "langchain"
    ],
    "rangkuman teks": [
        "text summarization", "extractive summarization",
        "abstractive summarization", "keyword extraction",
        "keybert", "topic modeling", "lda", "bertopic"
    ],

    # ── DATA SCIENCE ───────────────────────────────────────────────────
    "analisis data": [
        "data analysis", "statistik", "visualisasi data",
        "exploratory data analysis", "eda", "pandas", "numpy",
        "scipy", "deskriptif", "inferensial"
    ],
    "data mining": [
        "penggalian data", "association rule", "apriori", "fp growth",
        "clustering", "k means", "dbscan", "hierarchical clustering",
        "anomaly detection"
    ],
    "big data": [
        "hadoop", "spark", "apache kafka", "mapreduce",
        "data lake", "data warehouse", "batch processing",
        "stream processing", "etl"
    ],
    "prediksi": [
        "forecasting", "time series", "arima", "lstm forecasting",
        "regresi linier", "regresi logistik",
        "prediksi permintaan", "prophet"
    ],
    "preprocessing": [
        "data cleaning", "missing value", "outlier", "normalisasi",
        "standarisasi", "feature engineering", "feature selection",
        "imputasi", "one hot encoding", "label encoding"
    ],

    # ── WEB & MOBILE ───────────────────────────────────────────────────
    "pengembangan web": [
        "web development", "frontend", "backend", "fullstack",
        "rest api", "graphql", "react", "vue", "angular",
        "next.js", "typescript"
    ],
    "pengembangan mobile": [
        "mobile development", "android", "ios", "flutter",
        "react native", "kotlin", "swift",
        "progressive web app", "pwa", "cross platform"
    ],
    "ui ux": [
        "user interface", "user experience", "prototyping",
        "wireframe", "figma", "usability testing",
        "heuristic evaluation", "accessibility", "desain responsif"
    ],
    "e-commerce": [
        "toko online", "marketplace", "payment gateway",
        "keranjang belanja", "inventory management",
        "midtrans", "xendit", "order management"
    ],
    "web scraping": [
        "crawling", "selenium", "beautifulsoup", "scrapy",
        "puppeteer", "data extraction", "parsing html"
    ],

    # ── DATABASE & CLOUD ───────────────────────────────────────────────
    "basis data": [
        "database", "sql", "mysql", "postgresql", "sqlite",
        "nosql", "mongodb", "redis", "elasticsearch",
        "query optimization", "normalisasi database"
    ],
    "cloud computing": [
        "komputasi awan", "aws", "gcp", "azure",
        "iaas", "paas", "saas", "serverless",
        "cloud storage", "cloud deployment"
    ],
    "devops": [
        "ci cd", "docker", "kubernetes", "container",
        "pipeline", "github actions", "jenkins", "terraform",
        "infrastructure as code", "monitoring"
    ],
    "microservices": [
        "arsitektur layanan", "api gateway", "service mesh",
        "message broker", "rabbitmq", "load balancing", "scalability"
    ],

    # ── KEAMANAN & JARINGAN ────────────────────────────────────────────
    "keamanan siber": [
        "cybersecurity", "network security", "penetration testing",
        "vulnerability assessment", "enkripsi", "kriptografi",
        "ssl tls", "firewall", "ids ips"
    ],
    "kriptografi": [
        "encryption", "rsa", "aes", "hash function", "sha",
        "digital signature", "public key", "private key",
        "blockchain", "zero knowledge proof"
    ],
    "jaringan komputer": [
        "computer network", "tcp ip", "protokol", "routing",
        "switching", "lan wan", "vpn", "dns", "dhcp",
        "wireless network", "packet analysis"
    ],
    "iot": [
        "internet of things", "sensor", "mikrokontroler",
        "arduino", "raspberry pi", "mqtt", "embedded system",
        "smart device", "edge computing", "firmware"
    ],

    # ── SOFTWARE ENGINEERING ───────────────────────────────────────────
    "rekayasa perangkat lunak": [
        "software engineering", "sdlc", "agile", "scrum",
        "kanban", "waterfall", "software design",
        "software testing", "quality assurance"
    ],
    "pengujian perangkat lunak": [
        "software testing", "unit testing", "integration testing",
        "black box", "white box", "regression testing",
        "test case", "selenium", "automated testing"
    ],
    "sistem informasi": [
        "information system", "erp", "crm", "hris",
        "decision support system", "dss",
        "management information system", "enterprise system"
    ],
    "pemodelan sistem": [
        "uml", "use case", "class diagram", "sequence diagram",
        "activity diagram", "entity relationship diagram",
        "erd", "data flow diagram", "dfd"
    ],

    # ── GENERAL (tetap dari versi sebelumnya) ──────────────────────────
    "klasifikasi": ["classification", "kategorisasi", "pengelompokan"],
    "gambar":       ["image", "citra", "visual", "vision"],
}

# def ekspansi_query(teks, kamus=KAMUS_EKSPANSI):
#     teks_lower = teks.lower()
#     teks_ekspansi = teks_lower
#     sorted_keys = sorted(kamus.keys(), key=len, reverse=True)
#     for frasa in sorted_keys:
#         if frasa in teks_lower:
#             teks_ekspansi += " " + " ".join(kamus[frasa])
#     return teks_ekspansi