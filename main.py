import sys
import argparse
from src.ingestion import run_ingestion
from src.rag_engine import RAGAnalyst
from src.utils.doc_loader import ParsingStrategy

def main():
    parser = argparse.ArgumentParser(description="Ship Offline RAG System")
    subparsers = parser.add_subparsers(dest="command", help="Command to run")

    # Ingestion Command
    ingest_parser = subparsers.add_parser("ingest", help="Ingest documents")
    ingest_parser.add_argument("--strategy", type=str, default="table_heavy", 
                               choices=["fast_text", "table_heavy", "layout"],
                               help="Parsing strategy")

    # Analysis Command
    analyze_parser = subparsers.add_parser("analyze", help="Analyze an alarm situation")
    analyze_parser.add_argument("--code", type=str, required=True, help="Alarm Code")
    analyze_parser.add_argument("--temp", type=float, default=25.0, help="Sensor Temp")
    analyze_parser.add_argument("--pressure", type=float, default=101.3, help="Sensor Pressure")

    args = parser.parse_args()

    if args.command == "ingest":
        strategy_map = {
            "fast_text": ParsingStrategy.FAST_TEXT,
            "table_heavy": ParsingStrategy.TABLE_HEAVY,
            "layout": ParsingStrategy.LAYOUT_COMPLEX
        }
        run_ingestion(strategy_map[args.strategy])

    elif args.command == "analyze":
        analyst = RAGAnalyst()
        sensor_data = {"temperature": args.temp, "pressure": args.pressure}
        print(f"Analyzing {args.code} with data {sensor_data}...")
        result = analyst.analyze_situation(args.code, sensor_data)
        print("\n=== Analysis Result ===\n")
        print(result)

    else:
        parser.print_help()

if __name__ == "__main__":
    main()
