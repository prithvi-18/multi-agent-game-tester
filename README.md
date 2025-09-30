# 🎮 Multi-Agent Game Tester

An intelligent automated testing system that uses multiple AI agents to generate, rank, and execute comprehensive test cases for web games.

## ✨ Features

- **🤖 Multi-Agent Architecture**: PlannerAgent, RankerAgent, ExecutorAgent, and OrchestratorAgent
- **🎯 Game-Specific Testing**: Specialized for SumLink puzzle game
- **🌐 Web Interface**: Real-time status updates and comprehensive reporting  
- **📸 Screenshot Capture**: Visual evidence of test execution
- **🔄 Fallback Systems**: Robust handling of API quotas and browser issues
- **📊 Detailed Reports**: JSON reports with metrics and artifacts

## 🏗️ Architecture

Multi-Agent Game Tester
├── PlannerAgent → Generates test cases using GPT-3.5
├── RankerAgent → Prioritizes tests by importance
├── ExecutorAgent → Executes tests with Playwright
└── OrchestratorAgent → Coordinates all agents


## 🚀 Quick Start

### Prerequisites
- Python 3.13+
- OpenAI API Key (optional - has fallback mode)

### Installation

1. **Clone the repository**
2. **Create virtual environment**
3. **Install dependencies**
4. **Set up environment variables**


## 📊 Results

- **Success Rate**: 100% in simulation mode
- **Test Generation**: 5-20 candidate test cases
- **Execution Speed**: ~3-5 seconds per test
- **Artifacts**: Screenshots and detailed execution logs

## 🛠️ Technology Stack

- **Backend**: FastAPI, Python 3.13
- **AI/ML**: OpenAI GPT-3.5, LangChain  
- **Browser Automation**: Playwright
- **Frontend**: HTML5, JavaScript, CSS3
- **Testing**: Multi-agent orchestration

## 📁 Project Structure

multi-agent-game-tester/
├── app/
│ ├── agents/ # AI agents
│ ├── models/ # Data models
│ ├── services/ # Browser service
│ └── main.py # FastAPI app
├── frontend/ # Web interface
├── artifacts/ # Generated screenshots
├── requirements.txt # Dependencies
└── README.md



## 🎯 Demo

The system successfully:
1. 🤖 Generates game-specific test cases
2. 📊 Ranks tests by priority and feasibility  
3. 🚀 Executes tests with browser automation
4. 📸 Captures visual evidence
5. 📋 Generates comprehensive reports

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License.

## 🙏 Acknowledgments

- OpenAI for GPT-3.5 API
- Microsoft Playwright for browser automation
- FastAPI for the web framework
