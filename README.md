# QueryLens v0.1
An intuitive SQL parser that provides mental models, ASTs and clear English explanations to help learners and junior engineers/analysts onboard and upskill faster and more effectively!

## Directory Scaffold
query_lens/
│
├── src/
│   ├── __init__.py
│   └── parser.py          # initial tokeniser + parser logic
│
├── tests/
│   └── test_parser.py     # pytest with 2–3 assertions
│
├── README.md
├── LICENSE
├── .gitignore
└── requirements.txt       # pytest + optional rich if colour is desired!