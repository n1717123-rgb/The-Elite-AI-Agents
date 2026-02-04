# Contributing to The Elite AI Agents

Thank you for your interest in contributing!

## How to Contribute

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Run tests (`pytest`)
5. Commit (`git commit -m 'Add amazing feature'`)
6. Push (`git push origin feature/amazing-feature`)
7. Open a Pull Request

## Code Standards

- Python 3.11+
- Type hints required
- Docstrings for all public functions
- Follow existing code style

## Adding New Agents

1. Create directory in `agents/`
2. Follow the standard structure:
   ```
   agents/your-agent/
   ├── src/
   │   ├── agents/
   │   ├── models/
   │   ├── tools/
   │   └── utils/
   ├── tests/
   ├── app.py
   ├── requirements.txt
   └── README.md
   ```
3. Add entry to main README.md
4. Submit PR

## Questions?

Open an issue or reach out!
