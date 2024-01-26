import datetime
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy import DateTime
from sqlalchemy.orm import Session
from db import SessionLocal, Sikaku
 
app = FastAPI()
 
# データベースセッションの依存関数
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
 
@app.get("/list")
def get_sikaku_list(token: str, db: Session = Depends(get_db)):
    # データベースからすべての Exam レコードを取得
    sikakus = db.query(Sikaku).all()
    # 取得した Sikaku レコードを辞書のリストに変換して返す
    return sikakus
 
@app.get("/{ID}")
def get_sikaku_item(ID: str, token: str, db: Session = Depends(get_db)):
    # データベースから指定された exam_id の Sikaku レコードを取得
    sikaku = db.query(Sikaku).filter(Sikaku.exam_id == ID).first()
    if sikaku:
        # レコードが存在する場合は詳細情報を返す
        return {"exam_id": sikaku.exam_id, "exam_name": sikaku.exam_name, "pass_date": sikaku.pass_date}
    else:
        # レコードが存在しない場合は HTTP 404 エラーを返す
        raise HTTPException(status_code=404, detail="そんな試験は無いよ")
 
@app.post("/add")
def add_sikaku_item(ID: str, UID:str, NAME: str, DATE:datetime, token: str, db: Session = Depends(get_db)):
    # 新しい Sikaku レコードを作成してデータベースに追加
    new_sikaku = Sikaku(exam_id=ID, user_id=UID, exam_name=NAME, pass_date=DATE)
    if new_sikaku == "":
        return {"message": "空なのでエラー"}
    else:
        db.add(new_sikaku)
        # データベースの変更をコミット
        db.commit()
        # コミット後のデータをリフレッシュして、新しい Sikaku レコードの詳細情報を返す
        db.refresh(new_sikaku)
        return {"message": "Sikaku added successfully", "sikaku": {"exam_id": new_sikaku.exam_id, "user_id": new_sikaku.user_id, "exam_name": new_sikaku.exam_name, "pass_date": new_sikaku.pass_date}}
