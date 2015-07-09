# 'controller.py
from model import SaleOrder, ResPartner, ProductPricelist,\
                  PaymentTerm, FiscalOperationCategory, OlvSaleOrder
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

#----------------------------------------------------------------------
class Controller(object):

  def __init__(self, table_class, db_name):
    self.Table_Class= table_class 
    engine = create_engine(db_name, echo=True)
    Session = sessionmaker(bind=engine)
    self.session = Session()


  def addRecord(self,data):
    """
    """
    db_object = self.Table_Class() 
    for key in data:
      setattr(db_object,key,data[key]) 
    # connect to session and commit data to database
    self.session.add(db_object)
    self.session.commit()
    #session.close()
  
  def getAllRecords(self):
    """
    Get all records and return them
    """
    session = self.session 
    result = session.query(self.Table_Class).all()
    results = self.convertResults(result)
    #session.close()
    return results

  def deleteRecord(self,idNum):
    """
    Delete a record from the database
    """
    session = self.session
    record = session.query(self.Table_Class).filter_by(id=idNum).one()
    session.delete(record)
    session.commit()
    #session.close()

  def editRecord(self, idNum, row):
    """
    Edit a record
    """
    session = self.session
    record = session.query(self.Table_Class).filter_by(id=idNum).one()
    print
    db_object = self.Table_Class()
    for key in row:
      setattr(db_object,key,row[key])
    # connect to session and commit data to database
   
    session.add(db_object)
    session.commit()
    #session.close()
    
    
  #----------------------------------------------------------------------
  def convertResults(self,results):
    """
    Convert results to OlvBook objects
    """
    print
    olvRows = []
    for record in results:
        print record
        olvObject = record.toOlv() 
        olvRows.append(olvObject)
    return olvRows


  #----------------------------------------------------------------------
  def searchRecords(self, filterChoice, keyword):
    """
    Searches the database based on the filter chosen and the keyword
    given by the user

    TODO: foreign key filter
    """
    session = self.session
    tClass = self.Table_Class
    qry = session.query(tClass)
    result = qry.filter(getattr(tClass,filterChoice).contains('%s' % keyword)).all()
    rows = self.convertResults(result)

    return rows

if __name__=="__main__":
  
  so=Controller(SaleOrder,"sqlite:///odoo.db")
  data={ "name":"SO0002", 
         "date":"01-01-2014", 
         "partner_id":1, 
         "pricelist_id":1, 
         "payment_term_id":1,
         "fiscal_operation_category_id":1 }
  so.addRecord(data)
  rp=Controller(ResPartner,"sqlite:///odoo.db")
  data={ "name":"Alexandre",
         "ref": "0001",
         "name_ref" : "Alexandre [0001]" }
  rp.addRecord(data)  
  pl=Controller(ProductPricelist,"sqlite:///odoo.db") 
  data={ "name":"SPV" }
  pl.addRecord({ "name":"SPV" })

  pt=Controller(PaymentTerm,"sqlite:///odoo.db")
  pt.addRecord({ "name" : "28 dias"} )
  fc=Controller(FiscalOperationCategory,"sqlite:///odoo.db")
  fc.addRecord( { "name" : "Venda" })
         
  for olv in so.getAllRecords():
    print olv 

  for olv in so.searchRecords("name","0002"):
    print olv
