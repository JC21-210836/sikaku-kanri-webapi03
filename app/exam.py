from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from db import SessionLocal, Exam

app = FastAPI()

# データベースセッションの依存関数
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/list")
def get_exam_list(token: str, db: Session = Depends(get_db)):
    # データベースからすべての Exam レコードを取得
    exams = db.query(Exam).all()
    # 取得した Exam レコードを辞書のリストに変換して返す
    return exams

@app.get("/{ID}")
def get_exam_item(ID: str, token: str, db: Session = Depends(get_db)):
    # データベースから指定された exam_id の Exam レコードを取得
    exam = db.query(Exam).filter(Exam.exam_id == ID).first()
    if exam:
        # レコードが存在する場合は詳細情報を返す
        return {"exam_id": exam.exam_id, "exam_name": exam.exam_name}
    else:
        # レコードが存在しない場合は HTTP 404 エラーを返す
        raise HTTPException(status_code=404, detail="そんな試験は無いよ")

@app.post("/add")
def add_exam_item(ID: str, NAME: str, token: str, db: Session = Depends(get_db)):
    # 新しい Exam レコードを作成してデータベースに追加
    new_exam = Exam(exam_id=ID, exam_name=NAME)
    if new_exam == "":
        return {"message": "空なのでエラー"}
    else:
        db.add(new_exam)
        # データベースの変更をコミット
        db.commit()
        # コミット後のデータをリフレッシュして、新しい Exam レコードの詳細情報を返す
        db.refresh(new_exam)
        return {"message": "Exam added successfully", "exam": {"exam_id": new_exam.exam_id, "exam_name": new_exam.exam_name}}
