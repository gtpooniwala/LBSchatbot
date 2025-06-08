# LBS RAG Chatbot - Production Deployment Checklist

This checklist ensures the LBS RAG Chatbot is properly configured and ready for production deployment.

## 🚀 Pre-Deployment Checklist

### ✅ Code Quality & Testing
- [ ] All automated tests pass (`python test_system.py`)
- [ ] Manual testing completed across all query types
- [ ] Code review completed and approved
- [ ] Documentation updated and accurate
- [ ] Performance benchmarks meet requirements (<3s response time)
- [ ] Security review completed

### ✅ Environment Configuration
- [ ] Production environment variables configured
- [ ] OpenAI API key with sufficient quota
- [ ] CORS settings configured for production domains
- [ ] Rate limiting implemented and tested
- [ ] Logging configured appropriately (no sensitive data)
- [ ] Error handling tested and appropriate

### ✅ Infrastructure Setup
- [ ] Production server provisioned
- [ ] HTTPS certificates installed and configured
- [ ] Domain name configured and pointing to server
- [ ] Backup strategy implemented
- [ ] Monitoring and alerting configured
- [ ] Load balancing configured (if multiple instances)

### ✅ Knowledge Base & Data
- [ ] Knowledge base content reviewed and approved
- [ ] Contact information verified and up-to-date
- [ ] Emergency contact numbers tested
- [ ] Source links validated and accessible
- [ ] Embeddings cache generated and tested

### ✅ Security Configuration
- [ ] API keys stored securely (not in code)
- [ ] Server hardening completed
- [ ] Access controls implemented
- [ ] Audit logging enabled
- [ ] Data privacy compliance verified
- [ ] Input validation and sanitization tested

## 🔧 Production Configuration

### Environment Variables (.env)
```bash
# Production Flask Configuration
FLASK_ENV=production
FLASK_DEBUG=False
FLASK_HOST=0.0.0.0
FLASK_PORT=5003

# OpenAI Configuration
OPENAI_API_KEY=your_production_api_key
OPENAI_MODEL=gpt-3.5-turbo
OPENAI_MAX_TOKENS=1000
OPENAI_TEMPERATURE=0.7

# Security Settings
SECRET_KEY=your_secure_random_secret_key
RATE_LIMIT_PER_MINUTE=30
ALLOWED_ORIGINS=https://your-production-domain.com

# Logging Configuration
LOG_LEVEL=WARNING
LOG_FILE=/var/log/lbs-chatbot/app.log

# Performance Settings
SIMILARITY_THRESHOLD=0.3
TOP_K_DOCUMENTS=3
EMBEDDINGS_MODEL=sentence-transformers/all-MiniLM-L6-v2
```

### System Requirements
```
Minimum Server Specifications:
- CPU: 2 cores, 2.0 GHz
- RAM: 4 GB
- Storage: 20 GB SSD
- Network: 100 Mbps
- OS: Ubuntu 20.04 LTS or similar

Recommended Server Specifications:
- CPU: 4 cores, 2.5 GHz
- RAM: 8 GB
- Storage: 50 GB SSD
- Network: 1 Gbps
- OS: Ubuntu 22.04 LTS
```

## 🌐 Deployment Methods

### Method 1: Direct Server Deployment
```bash
# 1. Server Setup
sudo apt update && sudo apt upgrade -y
sudo apt install python3 python3-pip python3-venv nginx -y

# 2. Application Deployment
git clone <repository-url> /opt/lbs-chatbot
cd /opt/lbs-chatbot
python3 -m venv venv
source venv/bin/activate
pip install -r backend/requirements.txt

# 3. Configure Environment
cp backend/.env.example backend/.env
# Edit .env with production values

# 4. Test Application
cd backend
python app.py  # Should start without errors

# 5. Configure Process Manager (systemd)
sudo cp deployment/lbs-chatbot.service /etc/systemd/system/
sudo systemctl enable lbs-chatbot
sudo systemctl start lbs-chatbot

# 6. Configure Nginx
sudo cp deployment/nginx.conf /etc/nginx/sites-available/lbs-chatbot
sudo ln -s /etc/nginx/sites-available/lbs-chatbot /etc/nginx/sites-enabled/
sudo systemctl restart nginx
```

### Method 2: Docker Deployment
```bash
# Build and run with Docker
docker build -t lbs-chatbot .
docker run -d -p 80:80 --env-file .env lbs-chatbot

# Or use Docker Compose
docker-compose up -d
```

### Method 3: Cloud Platform Deployment

#### AWS Deployment
```bash
# Using AWS Elastic Beanstalk
eb init lbs-chatbot
eb create production
eb deploy
```

#### Google Cloud Deployment
```bash
# Using Google Cloud Run
gcloud run deploy lbs-chatbot --source .
```

#### Azure Deployment
```bash
# Using Azure App Service
az webapp up --name lbs-chatbot --resource-group myResourceGroup
```

## 🔒 Security Hardening

### Server Security
```bash
# 1. Firewall Configuration
sudo ufw enable
sudo ufw allow 22/tcp    # SSH
sudo ufw allow 80/tcp    # HTTP
sudo ufw allow 443/tcp   # HTTPS

# 2. SSL/TLS Configuration
sudo certbot --nginx -d your-domain.com

# 3. Security Headers (in nginx.conf)
add_header X-Frame-Options "SAMEORIGIN" always;
add_header X-Content-Type-Options "nosniff" always;
add_header Referrer-Policy "no-referrer-when-downgrade" always;
add_header Content-Security-Policy "default-src 'self' https:; script-src 'self'; style-src 'self' 'unsafe-inline';" always;

# 4. Rate Limiting (in nginx.conf)
limit_req_zone $binary_remote_addr zone=api:10m rate=10r/m;
limit_req zone=api burst=20 nodelay;
```

### Application Security
```python
# 1. Input Validation
from werkzeug.utils import secure_filename
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

# 2. Rate Limiting
limiter = Limiter(
    app,
    key_func=get_remote_address,
    default_limits=["200 per day", "50 per hour"]
)

# 3. CORS Configuration
CORS(app, origins=['https://your-production-domain.com'])

# 4. Error Handling (no sensitive info exposure)
@app.errorhandler(500)
def internal_error(error):
    return jsonify({'error': 'Internal server error'}), 500
```

## 📊 Monitoring & Alerting

### Health Monitoring
```bash
# 1. System Health Checks
# Create monitoring script: /opt/scripts/health-check.sh
#!/bin/bash
curl -f http://localhost:5003/health || exit 1

# 2. Log Monitoring
# Monitor for errors in application logs
tail -f /var/log/lbs-chatbot/app.log | grep ERROR

# 3. Resource Monitoring
# CPU, Memory, Disk usage monitoring
htop
df -h
free -m
```

### Application Monitoring
```python
# Add to app.py for basic metrics
import time
import logging

@app.before_request
def before_request():
    g.start_time = time.time()

@app.after_request
def after_request(response):
    duration = time.time() - g.start_time
    logging.info(f"Request completed in {duration:.2f}s")
    return response
```

### Alerting Setup
```bash
# Example: Simple email alerts for errors
# Add to crontab:
# */5 * * * * /opt/scripts/check-errors.sh

#!/bin/bash
# check-errors.sh
ERROR_COUNT=$(grep ERROR /var/log/lbs-chatbot/app.log | wc -l)
if [ $ERROR_COUNT -gt 10 ]; then
    echo "High error count: $ERROR_COUNT" | mail -s "LBS Chatbot Alert" admin@lbs.edu
fi
```

## 🔄 Backup & Recovery

### Database Backup (if applicable)
```bash
# For future database integration
pg_dump lbs_chatbot > backup_$(date +%Y%m%d).sql
```

### Application Backup
```bash
# 1. Knowledge Base Backup
cp backend/data/knowledge_base.txt /backup/knowledge_base_$(date +%Y%m%d).txt

# 2. Configuration Backup
cp backend/.env /backup/env_$(date +%Y%m%d).backup

# 3. Code Backup (Git)
git push origin main  # Ensure latest code is in repository
```

### Recovery Procedures
```bash
# 1. Quick Recovery (service restart)
sudo systemctl restart lbs-chatbot

# 2. Full Recovery (from backup)
git pull origin main
source venv/bin/activate
pip install -r backend/requirements.txt
sudo systemctl restart lbs-chatbot
```

## 📈 Performance Optimization

### Backend Optimization
```python
# 1. Caching Implementation
from functools import lru_cache

@lru_cache(maxsize=1000)
def get_cached_embedding(text):
    return model.encode(text)

# 2. Connection Pooling (for future database use)
from sqlalchemy import create_engine
engine = create_engine(DATABASE_URL, pool_size=20, max_overflow=0)

# 3. Async Processing (for future enhancement)
import asyncio
async def process_query_async(query):
    # Async query processing
    pass
```

### Frontend Optimization
```html
<!-- 1. Minify CSS/JS -->
<link rel="stylesheet" href="css/style.min.css">
<script src="js/script.min.js"></script>

<!-- 2. Enable Compression -->
<!-- Configure gzip in nginx.conf -->

<!-- 3. CDN Integration -->
<script src="https://cdn.jsdelivr.net/npm/library@version/lib.min.js"></script>
```

### Database Optimization (future)
```sql
-- Create indexes for faster queries
CREATE INDEX idx_embeddings_query ON embeddings(query_hash);
CREATE INDEX idx_chat_logs_timestamp ON chat_logs(timestamp);
```

## 🧪 Post-Deployment Testing

### Smoke Tests
```bash
# 1. Basic Connectivity
curl https://your-domain.com/health

# 2. API Functionality
curl -X POST https://your-domain.com/api/chat \
     -H "Content-Type: application/json" \
     -d '{"query": "What is the attendance policy?"}'

# 3. Frontend Loading
curl https://your-domain.com/ | grep "LBS"
```

### Load Testing
```bash
# Using Apache Bench
ab -n 1000 -c 10 https://your-domain.com/api/chat

# Using wrk
wrk -t12 -c400 -d30s https://your-domain.com/health
```

### User Acceptance Testing
```
Test Scenarios:
1. Normal academic queries (attendance, assignments, Canvas)
2. Support service inquiries (career, wellness, IT)
3. Sensitive content handling (mental health, harassment)
4. Mobile device compatibility
5. Browser compatibility (Chrome, Firefox, Safari, Edge)
6. Accessibility compliance (screen readers, keyboard navigation)
```

## 📞 Support & Maintenance

### Maintenance Schedule
```
Daily:
- [ ] Check system health endpoint
- [ ] Review error logs
- [ ] Monitor resource usage

Weekly:
- [ ] Review user feedback
- [ ] Update knowledge base if needed
- [ ] Security patch assessment

Monthly:
- [ ] Performance review
- [ ] Backup verification
- [ ] Dependency updates
- [ ] Security audit

Quarterly:
- [ ] Full system review
- [ ] Disaster recovery test
- [ ] User satisfaction survey
- [ ] Knowledge base content audit
```

### Emergency Procedures
```
System Down:
1. Check server status and logs
2. Restart application service
3. If unresolved, activate backup server
4. Notify stakeholders
5. Document incident

Data Loss:
1. Stop application immediately
2. Assess data loss scope
3. Restore from most recent backup
4. Verify data integrity
5. Resume operations
6. Conduct post-incident review

Security Incident:
1. Isolate affected systems
2. Document evidence
3. Notify security team
4. Patch vulnerability
5. Review and update security measures
```

### Contact Information
```
Technical Support:
- Primary: IT Department (+44 20 7000 7100)
- Secondary: System Administrator (admin@lbs.edu)
- Emergency: 24/7 IT Support (+44 20 7000 7999)

Business Support:
- Program Office: mam-mim@london.edu
- Student Wellness: wellness@london.edu
- Emergency: Campus Security (+44 20 7000 7888)
```

## ✅ Go-Live Checklist

### Final Verification
- [ ] All checklist items completed and verified
- [ ] Stakeholder approval obtained
- [ ] User training completed
- [ ] Support documentation distributed
- [ ] Backup procedures tested
- [ ] Rollback plan prepared
- [ ] Monitoring alerts configured
- [ ] Performance baselines established

### Launch Steps
1. [ ] Deploy to production environment
2. [ ] Run smoke tests
3. [ ] Enable monitoring and alerting
4. [ ] Notify users of availability
5. [ ] Monitor system closely for first 24 hours
6. [ ] Collect initial user feedback
7. [ ] Document any issues and resolutions

### Post-Launch
- [ ] Review deployment process for improvements
- [ ] Update documentation with any changes
- [ ] Schedule first maintenance window
- [ ] Plan feature enhancements based on user feedback

---

**Deployment Status**: ⏳ Pending
**Last Updated**: June 8, 2025
**Version**: 2.0
**Approved By**: [To be filled]
