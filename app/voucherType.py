from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from db import SessionLocal, VoucherType

app = FastAPI()
# データベースセッションの依存関数
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/list")
def get_vouchertype_list(token: str, db: Session = Depends(get_db)):
    # データベースからすべての VoucherType レコードを取得
    vouchertypes = db.query(VoucherType).all()
    # 取得した Exam レコードを辞書のリストに変換して返す
    return vouchertypes

@app.get("/{ID}")
def get_vouchertype_item(ID: str, token: str, db: Session = Depends(get_db)):
    # データベースから指定された exam_id の Exam レコードを取得
    vouchertype = db.query(VoucherType).filter(VoucherType.vouchertype_id == ID).first()
    if vouchertype:
        # レコードが存在する場合は詳細情報を返す
        return {"vouchertype_id": vouchertype.vouchertype_id, "vouchertype_name": vouchertype.vouchertype_name}
    else:
        # レコードが存在しない場合は HTTP 404 エラーを返す
        raise HTTPException(status_code=404, detail="そんな試験は無いよ")

@app.post("/add")
def add_vouchertype_item(ID: str, NAME: str, token: str, db: Session = Depends(get_db)):
    # 新しい VoucherType レコードを作成してデータベースに追加
    new_vouchertype = VoucherType(vouchertype_id=ID, vouchertype_name=NAME)
    if new_vouchertype == "":
        return {"message": "空なのでエラー"}
    else:
        db.add(new_vouchertype)
        # データベースの変更をコミット
        db.commit()
        # コミット後のデータをリフレッシュして、新しい VoucherType レコードの詳細情報を返す
        db.refresh(new_vouchertype)
        return {"message": "Vouchetyper added successfully", "vouchertype": {"vouchertype_id": new_vouchertype.vouchertype_id, "vouchertype_name": new_vouchertype.vouchertype_name}}