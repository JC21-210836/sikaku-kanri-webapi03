from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from db import SessionLocal, Voucher

app = FastAPI()

# データベースセッションの依存関数
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/list")
def get_voucher_list(token: str, db: Session = Depends(get_db)):
    # データベースからすべての Voucher レコードを取得
    vouchers = db.query(Voucher).all()
    # 取得した Voucher レコードを辞書のリストに変換して返す
    return [
        {"voucher_id": voucher.voucher_id, "deadline": voucher.deadline}
        for voucher in vouchers
    ]

@app.get("/{ID}")
def get_voucher_item(ID: str, token: str, db: Session = Depends(get_db)):
    # データベースから指定された voucher_id の Voucher レコードを取得
    voucher = db.query(Voucher).filter(Voucher.voucher_id == ID).first()
    if voucher:
        # レコードが存在する場合は詳細情報を返す
        return {"voucher_id": voucher.voucher_id, "deadline": voucher.deadline}
    else:
        # レコードが存在しない場合は HTTP 404 エラーを返す
        raise HTTPException(status_code=404, detail="そんな試験は無いよ")

@app.post("/add")
def add_voucher_item(ID: str, DATE: str, token: str, db: Session = Depends(get_db)):
    # 新しい Voucher レコードを作成してデータベースに追加
    new_voucher_item = Voucher(voucher_id=ID, deadline=DATE)
    if new_voucher_item == "":
        return {"message": "空なのでエラー"}
    else:
        db.add(new_voucher_item)
        # データベースの変更をコミット
        db.commit()
        # コミット後のデータをリフレッシュして、新しい Voucher レコードの詳細情報を返す
        db.refresh(new_voucher_item)
        return {
            "message": "Voucher added successfully", 
            "voucher_item": {
                "voucher_id": new_voucher_item.voucher_id,
                "deadline": new_voucher_item.deadline
            }
        }