from config.config import Settings
from chatbot_engine.vectorstore_builder import VectorStoreBuilder
from chatbot_engine.raft_preparation_pipeline import RAFTDataPreparationPipeline
from chatbot_engine.fine_tuning import FineTuning

from flask import Flask
from api.api import APIModule
from web.web import WebModule

import argparse

settings = Settings.load()

def run_engine_command(args):
    if args.task == "vectorstore-builder":
        builder = VectorStoreBuilder()
        builder.run()
        print("Vectorstore successfully built.")

    elif args.task == "raft-preparation-pipeline":
        pipeline = RAFTDataPreparationPipeline(
            api_key=settings.OPENAI_API_KEY,
            model=settings.FINE_TUNED_MODEL
        )
        pipeline.run_pipeline(target_phase=args.phase)
        print("RAFT data preparation pipeline completed.")

    elif args.task == "fine-tuning":
        ft = FineTuning(settings.OPENAI_API_KEY)
        ft.run()
        print("Fine-tuning process completed.")
    
def clean_engine_data_command(args):
    if args.task == "vectorstore":
        import shutil, os
        if os.path.exists("vectorstore/store"):
            shutil.rmtree("vectorstore/store")
            print("Vectorstore cleaned.")
        else:
            print("No vectorstore to clean.")

    elif args.task == "raft-data":
        import shutil, os
        if os.path.exists("./output/v2"):
            shutil.rmtree("./output/v2")
            print("RAFT fine-tuning data cleaned.")
        else:
            print("No RAFT dataset found.")

def run_web_app_command(args):
    if args.task == "app":
        app = Flask(__name__)

        web = WebModule()
        web.register_pages()

        api = APIModule()
        api.register_routes()

        app.register_blueprint(web.blueprint)
        app.register_blueprint(api.blueprint)

        print("Web app successfully ran.")
        app.run(host="0.0.0.0", port=5000, debug=True)

def main():
    parser = argparse.ArgumentParser(
        prog="chatbot-engine",
        description="Chatbot Engine CLI for RAFT pipeline, vectorstore, and fine-tuning tasks."
    )

    subparsers = parser.add_subparsers(dest="command", required=True)

    run_engine_parser = subparsers.add_parser("run-engine", description="Run a chatbot engine task")
    run_engine_parser.add_argument(
        "task",
        choices=["vectorstore-builder", "raft-preparation-pipeline", "fine-tuning"],
        help="Task to run"
    )
    run_engine_parser.add_argument(
        "--phase",
        type=int,
        default=None,
        help="Specific phase of the RAFT pipeline to run (1-5). Only applicable if task is 'raft-preparation-pipeline'."
    )
    run_engine_parser.set_defaults(func=run_engine_command)

    run_web_parser = subparsers.add_parser("run-web", description="Run a chatbot web app")
    run_web_parser.add_argument(
        "task",
        choices=["app"],
    )
    run_web_parser.set_defaults(func=run_web_app_command)

    clean_parser = subparsers.add_parser("clean", description="Clean generated data")
    clean_parser.add_argument(
        "task",
        choices=["vectorstore", "raft-data"],
        help="Which generated data to clean"
    )
    clean_parser.set_defaults(func=clean_engine_data_command)

    args = parser.parse_args()
    args.func(args)

if __name__ == "__main__":
    main()