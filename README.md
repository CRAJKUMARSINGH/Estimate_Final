# 🏗️ Construction Estimation System

A complete, production-ready construction cost estimation application with advanced features for project management, Excel import, and real-time calculations.

## ⚡ Quick Start

### Windows (Recommended)

1. Clone the repository
2. Run `setup.bat` to install dependencies
3. Run `run_unified_app.bat` to start the application

### Manual Installation

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run the application
streamlit run streamlit_app.py
```

### Docker

```bash
# Build and run with Docker Compose
docker-compose up -d

# Access at http://localhost:8501
```

## 🎯 Features

### Smart Import Wizard
- Multi-step process: Upload → Analyze → Preview → Import
- Real-time file analysis and validation
- SSR fuzzy matching with 90% accuracy
- Formula preservation from Excel
- Row selection and filtering
- Max file size: 5 MB, Max rows: 10,000

### Modern Dashboard
- Real-time project statistics
- Quick actions and shortcuts
- Visual progress tracking
- Recent activity timeline

### Real-time Calculations
- Instant updates across all items
- Multiple calculation types (Standard, Linear, Area, Volume, Circular)
- Dependency tracking
- Performance optimized for large datasets

### Database Integration
- Zero data loss with automatic saving
- Version history tracking
- Multi-project management
- Backup and recovery

### Visual Analytics
- Interactive cost breakdowns
- Progress tracking charts
- Summary reports
- PDF and CSV export

### Security Features
- Input validation and sanitization
- SQL injection prevention
- Path traversal protection
- Secure password hashing
- Session management

## 📋 Requirements

- Python 3.8 or higher
- 5 MB disk space for uploads
- Modern web browser

## 🔒 Security

This application implements:
- Parameterized SQL queries (SQLAlchemy)
- File upload validation (size, type, content)
- Input sanitization
- Secure file handling
- Environment variable configuration

## 📝 Configuration

Copy `.env.example` to `.env` and configure:

```bash
DATABASE_URL=sqlite:///construction_estimates.db
JWT_SECRET=your-secret-key-here
MAX_FILE_SIZE_MB=5
MAX_ROWS=10000
```

For Streamlit-specific settings, edit `.streamlit/secrets.toml` (not committed to git).

## 🐛 Troubleshooting

### Application won't start
1. Check Python version: `python --version` (must be 3.8+)
2. Reinstall dependencies: `pip install -r requirements.txt`
3. Check logs: `logs/app.log`

### Import fails
- Ensure file is under 5 MB
- Ensure file has fewer than 10,000 rows
- Check file format (.xlsx or .xls)
- Verify Excel file is not corrupted

### Performance issues
- Reduce number of items in estimate
- Close other browser tabs
- Check system resources

## � Poerformance

- Excel import: 1-2 seconds for typical files
- Real-time calculations: <0.1 seconds
- Database operations: <1 second
- Optimized for files up to 10,000 rows

## 🤝 Contributing

This is a production application. For issues or feature requests, contact: crajkumarsingh@hotmail.com

## 📄 License

MIT License - see LICENSE file for details

## � Version H istory

- v7.0 (2025-11) - Smart integration with security hardening
- v5.0 (2025-11) - Unified and consolidated
- Earlier versions - Feature development

## 📞 Support

Email: crajkumarsingh@hotmail.com

---

**Status**: Production Ready ✅  
**Last Updated**: November 2025
