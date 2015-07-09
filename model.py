#!/usr/bin/env python
# -*- coding: utf-8 -*-
# model.py

from sqlalchemy import Table, Column, create_engine
from sqlalchemy import Integer, ForeignKey, String, Unicode
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import backref, relation

engine = create_engine("sqlite:///odoo.db", echo=True)
DeclarativeBase = declarative_base(engine)
metadata = DeclarativeBase.metadata

########################################################################
class OlvSaleOrder(object):
    """
    Modelo de Pedidos para  ObjectListView
    """

    #----------------------------------------------------------------------
    #Variavel de Classe para formatação de views
    #----------------------------------------------------------------------
    formato=[ 
     { "label" : "Ordem", "align" : "left", "size" : 50, "field": "name" },
     { "label" : "Data", "align" : "left", "size" : 50, "field": "date" },
     { "label" : "Cliente", "align" : "center", "size" : 350, "field": "partner_ref" },
     { "label" : "Lista", "align" : "left", "size" : 50, "field": "pricelist" },
     { "label" : "Pagamento", "align" : "right", "size" : 100, "field": "payment_term" },
     { "label" : "Tipo", "align" : "right", "size" : 50, "field": "fiscal_operation_category" },
     
     ]
    #partner_ref=numero cliente (buscar partner_id no Odoo)
    #date= data do pedido
    #pricelist=lista de precos (pricelist_id)
    #payment_term=forma de pagamento
    #fiscal_operation_category=(venda|bonificação|troca)
    def __init__(self, id, partner_ref, date, pricelist, payment_term, 
                                                fiscal_operation_category):
        self.id = id  # unique row id from database
        self.partner_ref = partner_ref
        self.date = date # or now()
        self.pricelist = pricelist
        self.payment_term = payment_term
        self.fiscal_operation_category = fiscal_operation_category

    def __repr__(self):
        """"""
        return "<OlvSaleOrder: %d %s,%s,%s,%s,%s>" % (self.id, 
                                                      self.partner_ref, 
                                                      self.date, 
                                                      self.pricelist,
                                                      self.payment_term, 
                                                      self.fiscal_operation_category)

########################################################################
class SaleOrder(DeclarativeBase):
    """"""
    __tablename__ = "sale_order"
    
    id = Column(Integer, primary_key=True)
    name = Column("name", String(50)) #referencia da ordem no Odoo
    date = Column("date", String(50)) #data do pedido
    partner_id = Column(Integer, ForeignKey("res_partner.id"))
    pricelist_id = Column(Integer,ForeignKey("product_pricelist.id")) 
    payment_term_id = Column(Integer,ForeignKey("payment_term.id"))
    fiscal_operation_category_id = Column(Integer,
                                          ForeignKey("fiscal_operation_category.id"))
    
    partner=relation('ResPartner')    
    pricelist=relation('ProductPricelist')    
    payment_term=relation('PaymentTerm')    
    fiscal_operation_category=relation('FiscalOperationCategory')

    #----------------------------------------------------------------------
    def __repr__(self):
        """"""
        return "<SaleOrder: %s %s>" % (self.name, self.date)
    
    def toOlv(self):
      """
      Convert SaleOrder to OlvSaleOrder object
      """
      #id, partner_ref, date, pricelist, payment_term, fiscal_operation_category
      return  OlvSaleOrder(self.id, 
                           self.partner.name_ref,
                           self.date,
                           self.pricelist.name,
                           self.payment_term.name,
                           self.fiscal_operation_category.name,
                       )

########################################################################
class FiscalOperationCategory(DeclarativeBase):
    """Tipo de operacao (venda, bonificacao, troca, etc )"""
    __tablename__ = "fiscal_operation_category"
    
    id = Column(Integer, primary_key=True)
    name = Column("name", String(50)) 
        
    #----------------------------------------------------------------------
    def __repr__(self):
        """"""
        return "<PaymentTerm: %s %s>" % (self.name, self.name)

########################################################################
class PaymentTerm(DeclarativeBase):
    """"""
    __tablename__ = "payment_term"
    
    id = Column(Integer, primary_key=True)
    name = Column("name", String(50)) 
        
    #----------------------------------------------------------------------
    def __repr__(self):
        """"""
        return "<PaymentTerm: %s %s>" % (self.name, self.name)

########################################################################
class OrderLine(DeclarativeBase):
    """"""
    __tablename__ = "sale_order_line"
    
    id = Column(Integer, primary_key=True)
    product_id = Column(Integer, ForeignKey("product_product.id"))    
    #----------------------------------------------------------------------
    def __repr__(self):
        """"""
        return "<OrderLine: %s %s>" % (self.id, self.product_id)
    

########################################################################
class ProductProduct(DeclarativeBase):
    """"""
    __tablename__ = "product_product"
    
    id = Column(Integer, primary_key=True)
    name = Column("name", String(50))
    ref = Column("ref", String(50))
        
    #----------------------------------------------------------------------
    def __repr__(self):
        """"""
        return "<Product: %s %s>" % (self.name, self.ref)
    

########################################################################
class ResPartner(DeclarativeBase):
    """"""
    __tablename__ = "res_partner"
    
    id = Column(Integer, primary_key=True)
    name = Column("name", String(50))
    ref = Column("ref", String(50))
    name_ref=Column("name_ref", String(100))
        
    #----------------------------------------------------------------------
    def __repr__(self):
        """"""
        return "<ResPartner: %s %s>" % (self.name, self.ref)
    

########################################################################
class ProductPricelist(DeclarativeBase):
    """"""
    __tablename__ = "product_pricelist"
    
    id = Column(Integer, primary_key=True)
    name = Column("name", Unicode)
        
metadata.create_all()
