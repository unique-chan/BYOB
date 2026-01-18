import os
from pathlib import Path
from dotenv import load_dotenv

import shutil

from dump_arma.db_ingest import dump_arma_into_sql


if __name__ == "__main__":
    load_dotenv()
    db_url = os.getenv("DB_URL", "sqlite:///state.db")
    json_dir = Path(os.getenv("JSON_DIR", ".")).resolve()

    try:
        db_url_ = db_url.replace("sqlite:///", "").rsplit("/", 1)[0]
        os.makedirs(db_url_)
    except Exception as e:
        print(f'💽 {e}')
        answer = input(f'이미 저장된 Arma3 메타정보 DB가 존재합니다. 기존 DB를 삭제하고 진행하겠습니까? (Y/N): ')
        if answer.lower() == 'y':
            shutil.rmtree(db_url_)
            os.makedirs(db_url_)
        else:
            print(f'💽 프로그램을 종료합니다.')
            exit(0)

    dump_arma_into_sql(db_url, json_dir)