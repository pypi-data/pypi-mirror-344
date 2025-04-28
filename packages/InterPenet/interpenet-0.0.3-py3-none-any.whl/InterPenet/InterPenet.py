import tkinter as tk
from tkinter import ttk
#from Penetration import Penetration as pen
from . import Penetration as pen
import pandas as pd
import pickle
import matplotlib.pyplot as plt
import numpy as np
import os
from tkinter import filedialog
class Base():
    """貫通公式を管理するクラス
    """
    def read_pickle(self,fname):
        """
        fnameで示すファイルから辞書形式データを読み取り、戻り値で返す
        """
        with open(fname,'rb') as f:
            df = pickle.load(f)
        return df
    def write_pickle(self,fname,df):
        with open(fname, mode='wb') as f:
            pickle.dump(df,f)
    def setFormula(self,formula):
        """
        formulaに与える公式のインスタンスをself.formulaにセットする
        """
        self.formula=formula
    def getFormula(self):
        return self.formula
    def searchFormula(self,form='BRL'):
        """
        formの文字列と一致する公式オブジェクトをself.formulaにセットする
        """
        method=[
            'AlyLi',
            'BRL',
            'DeMarre',
            'Jowett',
            'Lambert',
            'Neilson',
            'Ohte',
            'SRI',
            'SwRI',
            'THOR',
            'WenJones'  
        ]
        if form not in method:
            return
        iFormula=method.index(form)
        if iFormula==0:
            formula=pen.AlyLi()
        if iFormula==1:
            formula=pen.BRL()
        if iFormula==2:
            formula=pen.DeMarre()
        if iFormula==3:
            formula=pen.Jowett()
        if iFormula==4:
            formula=pen.Lambert()
        if iFormula==5:
            formula=pen.Neilson()
        if iFormula==6:
            formula=pen.Ohte()
        if iFormula==7:
            formula=pen.SRI()
        if iFormula==8:
            formula=pen.SwRI()
        if iFormula==9:
            formula=pen.THOR()
        if iFormula==10:
            formula=pen.WenJones()
        self.formula=formula
    def cdata2ddata(self,title,ind,cdata):
        """
        title,描画インデックスind,cdataに基づきddataを構成し、もどす
        """
        dd={}
        dd['title']=title
        dd['ind']=ind
        dd['cdata']=cdata
        return dd
    def draw_graph(self,df2,cdata):
        df=df2.copy()
        self.searchFormula(form=df['formula'])
        self.formula.i_Valid=False  
        key=list(cdata.keys())
        var=key[0]
        df['v']['mean']=0
        div=cdata[var]['div']
        vmin=cdata[var]['min']
        vmax=cdata[var]['max']
        div=cdata[var]['div']
        var_r=np.linspace(vmin,vmax,div)
        vlim=[]
        for val in var_r:
            df[var]['mean']=val
            self.formula.Validation(df)
            vlim.append(self.formula.Gcheck(df))
        plt.xlabel(var)
        plt.xticks(rotation=45)
        plt.ylabel('Vbl(m/s)')
        plt.title(self.formula.title)
        plt.plot(var_r,vlim)
        plt.show()
    def draw_contour(self,df,ddata):
        """
        辞書型データdfの条件で、描画条件を指定する辞書型データddataに基づき等高線描画する
        """
        self.searchFormula(form=df['formula'])
        self.formula.i_Valid=False  
        self.formula.Validation(df)
        #if 'Material' in df.keys():
            #self.formula.setMaterial(df['Material'])
        cdata=ddata['cdata']
        key=list(cdata.keys())
        ii=ddata['ind']
        B,M,Z=self.formula.MakeContour(df,cdata)
        if ii==0:
            plt.pcolormesh(B, M, Z[ii], cmap='hsv',vmin=0.0,vmax=1.0)
        else:
            plt.pcolormesh(B, M, Z[ii], cmap='hsv')
        plt.title(ddata['title'])
        pp=plt.colorbar (orientation="vertical") # カラーバーの表示 
        plt.xlabel(key[0], fontsize=20)
        plt.ylabel(key[1], fontsize=20)
        plt.subplots_adjust(left=0.2,bottom=0.2)
        plt.show()
    def Calc_contour(self,df,ddata):
        """
        辞書型データdfの条件で、描画条件を指定する辞書型データddataに基づき等高線描画する
        """
        self.searchFormula(form=df['formula'])
        self.formula.i_Valid=False  
        self.formula.Validation(df)
        if 'Material' in df.keys():
            self.formula.setMaterial(df['Material'])
        cdata=ddata['cdata']
        key=list(cdata.keys())
        B,M,Z=self.formula.MakeContour(df,cdata)
        return B,M,Z
    def d_contour(self,B,M,Z,ddata,vmin,vmax):
        ii=ddata['ind']
        cdata=ddata['cdata']
        key=list(cdata.keys())
        plt.pcolormesh(B, M, Z[ii], cmap='hsv',vmin=vmin,vmax=vmax)
        plt.title(ddata['title'])
        pp=plt.colorbar (orientation="vertical") # カラーバーの表示 
        plt.xlabel(key[0], fontsize=20)
        plt.ylabel(key[1], fontsize=20)
        plt.subplots_adjust(left=0.2,bottom=0.2)
        plt.show()                   
    def Calc(self,df2):
        """
        辞書型データに基づき確率論的評価を行い、結果を出力する
        """
        dict={}
        df=df2.copy()
        self.searchFormula(form=df['formula'])
        self.formula.i_Valid=True

        ##################################################
        #つまり、クラスGに特殊処理があるとき、貫通公式にはgDict関数を、クラスGには、setDict関数をもつ必要がある。
        ##################################################
        self.formula.Validation(df)
        print('*** Probabilistic analysis ***')
        print('[',self.formula.GetTitle(),']')
        print('variable=',self.formula.variable)
        #print('value=',self.formula.Gcheck(df))#確率変数の平均値に対するg値評価

        self.formula.Calc(df)#信頼性評価
        print('beta=',self.formula.GetBeta())#信頼性指標の出力
        print('Alpha=',self.formula.GetAlpha())#感度の出力
        print('Pf=',self.formula.GetPOF())#破損確率の出力
        print('*** Analysis of Balistic Limit Velocity ***')
        df['v']['mean']=0
        df['Me']['mean']=1.0
        mu,sig,dist=self.formula.makeData(df)
        print('Vbl=',self.formula.gcalc(mu))
    def CalcDict(self,df2):
        """
        Calcと同じ機能であるが、辞書型データに出力しもどす
        """
        dict={}
        res={}
        df=df2.copy()
        self.searchFormula(form=df['formula'])
        ##################################################
        #つまり、クラスGに特殊処理があるとき、貫通公式にはgDict関数を、クラスGには、setDict関数をもつ必要がある。
        ##################################################
        form=df['formula']
        res[form]={}
        self.formula.i_Valid=False
        if 'Material' in df.keys():
            self.formula.setMaterial(df['Material'])
            res[form]['Material']=df['Material']
        if 'shape' in df.keys():
            res[form]['shape']=df['shape']
        res[form]['unsatisfied']=self.formula.Validation(df)
        res[form]['variable']=self.formula.variable
        mu,sig,dist=self.formula.makeData(df)
        res[form]['value']=self.formula.gcalc(mu)
        self.formula.Reliability(df,dict=dict)#信頼性評価
        res[form]['beta']=self.formula.GetBeta()
        res[form]['Alpha']=self.formula.GetAlpha()
        res[form]['Pf']=self.formula.GetPOF()
        vv=df['v']['mean']
        df['v']['mean']=0
        res[form]['Vbl']=self.formula.Gcheck(df)
        df['v']['mean']=vv
        return res
    def Vbl(self,df):
        """
        辞書型データで与えられる入力条件dfについて、限界速度の計算を行い、結果を出力する
        """
        
        self.searchFormula(form=df['formula'])
        self.formula.SaveDf(df)
        self.formula.i_Valid=True
        df2=df.copy()
        print('*** Analysis of Balistic Limit Velocity ***')
        print('[',self.formula.GetTitle(),']')
        df2['v']['mean']=0
        df2['Me']['mean']=1.0
        mu=self.formula.makeMean(df2)
        print('Vbl=',self.formula.gcalc(mu))
    def apCalc(self):
        """
        辞書型データself.dfに対して確率論的評価を行い、結果を出力する
        """
        self.Calc(self.df)
    def setDf(self,df):
        """
        辞書型データdfをself.dfにセットする
        """
        self.df=df
    def getDf(self):
        return self.df
    def CalcPenet(self,fname):
        """
        fnameで与えられるpickle型データから辞書型データを読み込み、確率論的計算を行って、結果を出力する
        """
        df = self.read_pickle(fname)
        self.Calc(df)
        print('File=',fname)      

import sys
from io import StringIO       
class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.original_stdout = sys.stdout#標準出力の出力先
        self.bb=Base()
        self.master = master
        self.method=[
            'AlyLi',
            'BRL',
            'DeMarre',
            'Jowett',
            'Lambert',
            'Neilson',
            'Ohte',
            'SRI',
            'SwRI',
            'THOR',
            'WenJones'  
        ]
        self.dict={}#貫通公式管理クラスに特殊処理があるときに引き渡す辞書データ
        lbl = tk.Label(text='Formula')
        lbl.place(x=20,y=10)
        # チェックボックスON/OFFの状態

        self.var_item = tk.IntVar() #formulaの選択項目
        self.out_item = tk.IntVar() #出力先の選択項目
        self.var_prob=tk.IntVar()
        self.var_draw=tk.IntVar()
        self.xcoord_item=tk.IntVar()
        self.ycoord_item=tk.IntVar()
        #手法の設定
        for i in range(len(self.method)):
            btn=tk.Radiobutton(self.master,value=i, variable=self.var_item,text=self.method[i],command=self.change_selected_item) 
            btn.place(x=10, y=30 + (i * 24))
        self.btn_v=tk.Radiobutton(self.master,value=0,variable=self.var_prob,text='Evaluate v_lim',command=self.change_anal_item)
        self.btn_p=tk.Radiobutton(self.master,value=1,variable=self.var_prob,text='Probabilistic analysis',command=self.change_anal_item)
        self.btn_contour=tk.Radiobutton(self.master,value=0,variable=self.var_draw,text='Contour',command=self.change_contour_item)
        self.btn_graph=tk.Radiobutton(self.master,value=1,variable=self.var_draw,text='Graph',command=self.change_contour_item)
        #self.var=['b', 'd', 'm', 'Su', 'Sy','Lsh', 'th', 'Limp', 'v','ro_imp','a10','shape','fragment','Material']
        self.var=['b', 'd', 'm', 'Su', 'Sy','Lsh', 'th', 'Limp', 'v','ro_imp','shape','fragment','Material','Me']
        lbl_out = tk.Label(text='Output')#printの出力先ラジオのラベル
        lbl_b = tk.Label(text='b'); self.lbl_b=tk.Label(text='*')
        lbl_d = tk.Label(text='d'); self.lbl_d=tk.Label(text='*')
        lbl_m = tk.Label(text='m'); self.lbl_m=tk.Label(text='*')
        lbl_Su = tk.Label(text='Su'); self.lbl_Su=tk.Label(text='*')
        lbl_Sy = tk.Label(text='Sy'); self.lbl_Sy=tk.Label(text='*')
        lbl_Lsh = tk.Label(text='Lsh'); self.lbl_Lsh=tk.Label(text='*')
        lbl_th = tk.Label(text='th'); self.lbl_th=tk.Label(text='*')
        lbl_Limp = tk.Label(text='Limp'); self.lbl_Limp=tk.Label(text='*')
        lbl_v = tk.Label(text='v'); self.lbl_v=tk.Label(text='*')
        lbl_ro_imp = tk.Label(text='ro_imp'); self.lbl_ro_imp=tk.Label(text='*')
        lbl_a10 = tk.Label(text='a10'); self.lbl_a10=tk.Label(text='*')
        lbl_shape=tk.Label(text='Shape');self.lbl_shape=tk.Label(text='*')
        lbl_frag=tk.Label(text='Fragment');self.lbl_frag=tk.Label(text='*')
        lbl_Material=tk.Label(text='Material');self.lbl_Material=tk.Label(text='*')
        lbl_Me = tk.Label(text='Me');self.lbl_Me=tk.Label(text='*')
        lbl_const=tk.Label(text='Const.')
        lbl_mean=tk.Label(text='Mean')
        lbl_cov=tk.Label(text='COV')
        lbl_dist=tk.Label(text='Distribution')

        en=15
        self.txt_b_m = tk.Entry(width=en)
        self.txt_d_m = tk.Entry(width=en)
        self.txt_m_m = tk.Entry(width=en)
        self.txt_Su_m = tk.Entry(width=en)
        self.txt_Sy_m = tk.Entry(width=en)
        self.txt_Lsh_m = tk.Entry(width=en)
        self.txt_th_m = tk.Entry(width=en)
        self.txt_Limp_m = tk.Entry(width=en)
        self.txt_v_m = tk.Entry(width=en)
        self.txt_Me_m= tk.Entry(width=en)
        self.txt_b_c = tk.Entry(width=en)
        self.txt_d_c = tk.Entry(width=en)
        self.txt_m_c = tk.Entry(width=en)
        self.txt_Su_c = tk.Entry(width=en)
        self.txt_Sy_c = tk.Entry(width=en)
        self.txt_Lsh_c = tk.Entry(width=en)
        self.txt_th_c = tk.Entry(width=en)
        self.txt_Limp_c = tk.Entry(width=en)
        self.txt_v_c = tk.Entry(width=en)
        self.txt_Me_c = tk.Entry(width=en)
        self.txt_ro_imp=tk.Entry(width=en)
        
        #self.txt_a10=tk.Entry(width=en*2)
        #self.txt_shape=tk.Entry(width=en*2)
        self.combo_shape=ttk.Combobox(width=en,values=['none'])
        #self.txt_frag=tk.Entry(width=en*2)
        self.combo_frag=ttk.Combobox(width=en,values=['none'])
        self.combo_mat=ttk.Combobox(width=en,values=['none'])
        self.combo_item=ttk.Combobox(width=en,values=['none'])
        self.combo_item.bind('<<ComboboxSelected>>', self.comboSelected)
        #self.txt_Text=tk.Text(height=25,width=70)
        dist=['normal','lognormal','gumbel','weibul','uniform']
        en1=10
        self.combo_b=ttk.Combobox(width=en1,values=dist)
        self.combo_d=ttk.Combobox(width=en1,values=dist)
        self.combo_m=ttk.Combobox(width=en1,values=dist)
        self.combo_Su=ttk.Combobox(width=en1,values=dist)
        self.combo_Sy=ttk.Combobox(width=en1,values=dist)
        self.combo_Lsh=ttk.Combobox(width=en1,values=dist)
        self.combo_th=ttk.Combobox(width=en1,values=dist)
        self.combo_Limp=ttk.Combobox(width=en1,values=dist)
        self.combo_v=ttk.Combobox(width=en1,values=dist)
        self.combo_Me=ttk.Combobox(width=en1,values=dist)
        lbl_title=tk.Label(text='Title')
        self.txt_title=tk.Entry(width=en*5)
        self.button_calc = tk.Button(self.master, text = "Calc", command = self.Calc_click)
        self.button_draw=tk.Button(self.master,text="Draw",command=self.Draw_click)
        self.button_draw.config(state='disabled')
        button_load= tk.Button(self.master, text = "Load", command = self.Load_click)
        self.txt_load=tk.Entry(width=en)
        button_save= tk.Button(self.master, text = "Save", command = self.Save_click)
        button_exit=tk.Button(self.master,text="Exit",command=self.master.destroy)
        self.txt_save=tk.Entry(width=en)
        i=0; xx=150; x_ast=xx-10; yy=30; dy_ast=3; dx0=50; dx=100
        button_exit.place(x=30,y=30 + (len(self.method) * 24)+70)
        #self.txt_Text.place(x=xx+260,y=yy)
        lbl_out.place(x=xx+dx0*15+10,y=yy-24+24+350)#printの出力先ラジオのラベル
        radio1=tk.Radiobutton(self.master,value=0, variable=self.out_item,text='Panel',command=self.change_out_item)
        radio1.place(x=xx+dx0*15+10,y=yy-24+24+24+350)
        radio2=tk.Radiobutton(self.master,value=1, variable=self.out_item,text='stdOutput',command=self.change_out_item)
        radio2.place(x=xx+dx0*15+10,y=yy-24+24+24+24+350)
        lbl_const.place(x=xx-30,y=yy-24)
        lbl_mean.place(x=xx+dx0,y=yy-24)
        lbl_cov.place(x=xx+dx0+dx,y=yy-24)
        lbl_dist.place(x=xx+dx0+dx+dx,y=yy-24)
        lbl_b.place(x=xx,y=yy);  self.lbl_b.place(x=x_ast,y=yy+dy_ast);i+=1
        self.txt_b_m.place(x=xx+dx0,y=yy)
        self.txt_b_c.place(x=xx+dx0+dx,y=yy)
        self.combo_b.place(x=xx+dx0+dx+dx,y=yy)
        yy+=24;lbl_d.place(x=xx,y=yy); self.lbl_d.place(x=x_ast,y=yy+dy_ast);i+=1
        self.txt_d_m.place(x=xx+dx0,y=yy)
        self.txt_d_c.place(x=xx+dx0+dx,y=yy)
        self.combo_d.place(x=xx+dx0+dx+dx,y=yy)
        yy+=24;lbl_m.place(x=xx,y=yy); self.lbl_m.place(x=x_ast,y=yy+dy_ast);i+=1
        self.txt_m_m.place(x=xx+dx0,y=yy)
        self.txt_m_c.place(x=xx+dx0+dx,y=yy)
        self.combo_m.place(x=xx+dx0+dx+dx,y=yy)
        yy+=24;lbl_Su.place(x=xx,y=yy); self.lbl_Su.place(x=x_ast,y=yy+dy_ast);i+=1
        self.txt_Su_m.place(x=xx+dx0,y=yy)
        self.txt_Su_c.place(x=xx+dx0+dx,y=yy)
        self.combo_Su.place(x=xx+dx0+dx+dx,y=yy)
        yy+=24;lbl_Sy.place(x=xx,y=yy); self.lbl_Sy.place(x=x_ast,y=yy+dy_ast);i+=1
        self.txt_Sy_m.place(x=xx+dx0,y=yy)
        self.txt_Sy_c.place(x=xx+dx0+dx,y=yy)
        self.combo_Sy.place(x=xx+dx0+dx+dx,y=yy)
        yy+=24;lbl_Lsh.place(x=xx,y=yy); self.lbl_Lsh.place(x=x_ast,y=yy+dy_ast);i+=1
        self.txt_Lsh_m.place(x=xx+dx0,y=yy)
        self.txt_Lsh_c.place(x=xx+dx0+dx,y=yy)
        self.combo_Lsh.place(x=xx+dx0+dx+dx,y=yy)
        yy+=24;lbl_th.place(x=xx,y=yy); self.lbl_th.place(x=x_ast,y=yy+dy_ast);i+=1
        self.txt_th_m.place(x=xx+dx0,y=yy)
        self.txt_th_c.place(x=xx+dx0+dx,y=yy)
        self.combo_th.place(x=xx+dx0+dx+dx,y=yy)
        yy+=24;lbl_Limp.place(x=xx,y=yy); self.lbl_Limp.place(x=x_ast,y=yy+dy_ast);i+=1
        self.txt_Limp_m.place(x=xx+dx0,y=yy)
        self.txt_Limp_c.place(x=xx+dx0+dx,y=yy)
        self.combo_Limp.place(x=xx+dx0+dx+dx,y=yy)
        yy+=24;lbl_v.place(x=xx,y=yy); self.lbl_v.place(x=x_ast,y=yy+dy_ast);i+=1
        self.txt_v_m.place(x=xx+dx0,y=yy)
        self.txt_v_c.place(x=xx+dx0+dx,y=yy)
        self.combo_v.place(x=xx+dx0+dx+dx,y=yy)
        yy+=24;lbl_Me.place(x=xx,y=yy); self.lbl_Me.place(x=x_ast,y=yy+dy_ast);i+=1
        self.txt_Me_m.place(x=xx+dx0,y=yy)
        self.txt_Me_c.place(x=xx+dx0+dx,y=yy)
        self.combo_Me.place(x=xx+dx0+dx+dx,y=yy)        
        yy+=24;lbl_ro_imp.place(x=xx,y=yy); self.lbl_ro_imp.place(x=x_ast,y=yy+dy_ast);i+=1
        self.txt_ro_imp.place(x=xx+dx0,y=yy)
        #yy+=24;lbl_a10.place(x=xx,y=yy); self.lbl_a10.place(x=x_ast,y=yy+dy_ast);i+=1
        #self.txt_a10.place(x=xx+dx0,y=yy)
        yy+=24;lbl_shape.place(x=xx,y=yy); self.lbl_shape.place(x=x_ast,y=yy+dy_ast);i+=1
        self.combo_shape.place(x=xx+dx0,y=yy)
        yy+=24;lbl_frag.place(x=xx,y=yy); self.lbl_frag.place(x=x_ast,y=yy+dy_ast);i+=1
        self.combo_frag.place(x=xx+dx0,y=yy)
        yy+=24;lbl_Material.place(x=xx,y=yy); self.lbl_Material.place(x=x_ast,y=yy+dy_ast);i+=1
        self.combo_mat.place(x=xx+dx0,y=yy)

        yy+=48
        
        yy+=48; lbl_title.place(x=xx,y=yy); self.txt_title.place(x=xx+dx0,y=yy)
        yy+=48; 
        yy+=48; button_load.place(x=xx,y=yy); self.txt_load.place(x=xx+dx0,y=yy)
        yy+=48; button_save.place(x=xx,y=yy); self.txt_save.place(x=xx+dx0,y=yy)


        #self.change_selected_item()
    def comboSelected(self,Wig):
        ii=self.combo_item.current()
        vmax=np.max(self.Z[ii])
        vmin=np.min(self.Z[ii])
        self.vv_min.delete(0,tk.END)
        self.vv_max.delete(0,tk.END)
        self.vv_min.insert(0,'{:.3e}'.format(vmin))
        self.vv_max.insert(0,'{:.3e}'.format(vmax))
    def Draw_click(self):
        self.formula.i_Valid=False
        cdata=self.MakeCdata()
        data=self.MakeDict()
        self.formula.Validation(data)
        if 'Material' in data.keys():
            self.formula.setMaterial(data['Material'])
        key=list(cdata.keys())
        if self.var_draw.get()==0:
            #等高線描画
            ii=self.combo_item.current()
            var=self.combo_item.get()
            ddata1=self.bb.cdata2ddata(var,ii,cdata)
            #self.bb.draw_contour(data,ddata1)
            vmin=self.vv_min.get()
            vmax=self.vv_max.get()
            self.bb.d_contour(self.B,self.M,self.Z,ddata1,vmin,vmax)
        if self.var_draw.get()==1:
            # 限界速度の描画
            df=self.MakeDict()
            cdata=self.MakeCdata()
            self.bb.draw_graph(df,cdata)



    def MakeCdata(self):
        i_x=self.xcoord_item.get()
        cdata={}
        self.make(cdata,i_x)
        if self.var_draw.get()==1:
            return cdata
        i_y=self.ycoord_item.get()
        self.make(cdata,i_y)
        return cdata
    def make(self,cdata,ii):
        if ii==0:
            self.makedata(cdata,'b',self.b_min.get(),self.b_max.get(),self.b_div.get())
        if ii==1:
            self.makedata(cdata,'d',self.d_min.get(),self.d_max.get(),self.d_div.get())
        if ii==2:
            self.makedata(cdata,'m',self.m_min.get(),self.m_max.get(),self.m_div.get())
        if ii==3:
            self.makedata(cdata,'Su',self.Su_min.get(),self.Su_max.get(),self.Su_div.get())
        if ii==4:
            self.makedata(cdata,'Sy',self.Sy_min.get(),self.Sy_max.get(),self.Sy_div.get())
        if ii==5:
            self.makedata(cdata,'Lsh',self.Lsh_min.get(),self.Lsh_max.get(),self.Lsh_div.get())
        if ii==6:
            self.makedata(cdata,'th',self.th_min.get(),self.th_max.get(),self.th_div.get())
        if ii==7:
            self.makedata(cdata,'Limp',self.Limp_min.get(),self.Limp_max.get(),self.Limp_div.get())
        if ii==8:
            self.makedata(cdata,'v',self.v_min.get(),self.v_max.get(),self.v_div.get())
    def makedata(self,cdata,c,v_min,v_max,v_div):
        cdata[c]={}
        cdata[c]['min']=float(v_min)
        cdata[c]['max']=float(v_max)
        cdata[c]['div']=int(v_div)
    def change_contour_item(self):
        if self.var_draw.get()==0:
            self.combo_item.config(state='normal')
            self.makeItem()
        else:
            self.combo_item.config(state='disabled')
        i_x=self.xcoord_item.get()
        i_y=self.ycoord_item.get()
        self.mod(self.b_min,self.b_max,self.b_div,i_x,i_y,0)
        self.mod(self.d_min,self.d_max,self.d_div,i_x,i_y,1)
        self.mod(self.m_min,self.m_max,self.m_div,i_x,i_y,2)
        self.mod(self.Su_min,self.Su_max,self.Su_div,i_x,i_y,3) 
        self.mod(self.Sy_min,self.Sy_max,self.Sy_div,i_x,i_y,4) 
        self.mod(self.Lsh_min,self.Lsh_max,self.Lsh_div,i_x,i_y,5)
        self.mod(self.th_min,self.th_max,self.th_div,i_x,i_y,6)
        self.mod(self.Limp_min,self.Limp_max,self.Limp_div,i_x,i_y,7)
        self.mod(self.v_min,self.v_max,self.v_div,i_x,i_y,8)             
    def mod(self,o_min,o_max,o_div,i_x,i_y,ii):
        o_min['state']='disable'
        o_max['state']='disable'
        o_div['state']='disable'
        if i_x==ii:
            o_min['state']='normal'
            o_max['state']='normal'
            o_div['state']='normal'
        if self.var_draw.get()==0 and i_y==ii:
            o_min['state']='normal'
            o_max['state']='normal'
            o_div['state']='normal'        
    def Save_click(self):
        df=self.MakeDict()
        fname=self.txt_save.get()
        self.bb.write_pickle(fname,df)
    def Load_click(self):
        #fname=self.txt_load.get()
        fname=self.select()
        df = self.bb.read_pickle(fname)#ファイルから辞書型データdfに読み込む
        #self.bbはクラスBaseのインスタンス
        self.bb.setDf(df)#辞書型データをself.bbに保存
        self.toDict(df)
        self.txt_load.insert(0,fname)#ファイル名をテキストボックスに表示
        print('***reading file[',fname,']') 
    def select(self):
    # 選択可能な拡張子を指定
        filetype = [("Pickle file", ".pkl")]
        # ファイル選択の初期表示のディレクトリ
        #path = os.path.abspath(os.path.dirname(__file__))
        path = os.path.abspath(os.path.dirname(__name__))
        # ファイル選択ダイアログ表示
        cap_filepath = filedialog.askopenfilename(filetype = filetype, initialdir = path)
        # Widgetにbindされた変数にファイル名を設定
        filename = os.path.basename(cap_filepath)
        #cap_filename.set( filename )
        return filename       
    def Calc_click(self):
        #self.change_out_item()
        if self.master.title()=='Drawing system':
            self.formula.i_Valid=False
            cdata=self.MakeCdata()
            data=self.MakeDict()
            self.formula.Validation(data)
            if 'Material' in data.keys():
                self.formula.setMaterial(data['Material'])
            key=list(cdata.keys())
            if self.var_draw.get()==0:
                #等高線描画
                ii=self.combo_item.current()
                var=self.combo_item.get()
                ddata1=self.bb.cdata2ddata(var,ii,cdata)
                B,M,Z=self.bb.Calc_contour(data,ddata1)
                self.B=B
                self.M=M
                self.Z=Z
                self.lbl_item.config(state='normal')
                self.button_draw.config(state='normal')
                self.combo_item.config(state='normal')
                #self.combo_item.set('PoF')
                #self.bb.d_contour(B,M,Z,ddata1)
                #self.bb.draw_contour(data,ddata1)
            if self.var_draw.get()==1:
                # 限界速度の描画
                cdata=self.MakeCdata() 
                df=self.MakeDict()
                #self.bb.draw_graph(df,cdata)
        else:
            # Replace stdout with a StringIO object
            iOut=self.out_item.get()
            if iOut==0:
                sys.stdout = StringIO()              
            df=self.MakeDict()
            self.df=df
            print('==========================================')
            print('Title:',self.txt_title.get())
            if self.iProb==1:
                self.bb.Calc(df) #self.bbはBase()のインスタンス
            else:
                df['v']['mean']=0#限界速度計算のときには、入力速度=0として計算
                self.bb.Vbl(df)#dfにはmeanしか入っていないことに注意
            #iOut=self.out_item.get()
            if iOut==0:
                self.txt_Text.insert(1.0,sys.stdout.getvalue()) 
    def MakeDict(self):
        df={}
        df=self.dfAdd(df)
        df=self.dfAddC(df)
        df['Title']=self.txt_title.get()
        df['formula']=self.method[self.var_item.get()]
        if df['formula']=='Jowett':
            self.dict['Lsh']=df['Lsh']
        return df
    def Clear(self):
        self.txt_title.delete(0,tk.END)
        self.txt_b_m.delete(0,tk.END)
        self.txt_b_c.delete(0,tk.END)
        self.txt_d_m.delete(0,tk.END)
        self.txt_d_c.delete(0,tk.END)
        self.txt_m_m.delete(0,tk.END)
        self.txt_m_c.delete(0,tk.END)
        self.txt_Su_m.delete(0,tk.END)
        self.txt_Su_c.delete(0,tk.END)
        self.txt_Sy_m.delete(0,tk.END)
        self.txt_Sy_c.delete(0,tk.END)
        self.txt_Lsh_m.delete(0,tk.END)
        self.txt_Lsh_c.delete(0,tk.END)
        self.txt_th_m.delete(0,tk.END)
        self.txt_th_c.delete(0,tk.END)
        self.txt_Limp_m.delete(0,tk.END)
        self.txt_Limp_c.delete(0,tk.END)
        self.txt_v_m.delete(0,tk.END)
        self.txt_v_c.delete(0,tk.END)
        self.txt_ro_imp.delete(0,tk.END)
        self.txt_Me_m.delete(0,tk.END)
        self.txt_Me_c.delete(0,tk.END)
        self.txt_load.delete(0,tk.END)
        #self.txt_a10.delete(0,tk.END)
        #self.combo_shape.delete(0,tk.END)
        #self.combo_frag.delete(0,tk.END)

    def toDict(self,df):
        self.Clear()
        self.var_item.set(self.method.index(df['formula']))
        self.change_selected_item()
        self.txt_title.insert(0,df['Title'])
        dist=['normal','lognormal','gumbel','weibul','uniform']
        for i in range(len(self.formula.variable)):
            var=self.formula.variable[i]
            ii=self.var.index(var)#登録されている変数self.varの中の何番目かを示すインデックス
            if ii==0:
                self.txt_b_m.insert(0,df['b']['mean']) 
                if 'cov' in list(df['b'].keys()):
                    self.txt_b_c.insert(0,df['b']['cov'])
                    ii=dist.index(df['b']['dist'])
                    self.combo_b.current(ii)
            if ii==1:
                self.txt_d_m.insert(0,df['d']['mean'])
                if 'cov' in list(df['d'].keys()):
                    self.txt_d_c.insert(0,df['d']['cov'])
                    ii=dist.index(df['d']['dist'])
                    self.combo_d.current(ii)
            if ii==2:
                self.txt_m_m.insert(0,df['m']['mean'])
                if 'cov' in list(df['m'].keys()):
                    self.txt_m_c.insert(0,df['m']['cov'])
                    ii=dist.index(df['m']['dist'])
                    self.combo_m.current(ii)
            if ii==3:
                self.txt_Su_m.insert(0,df['Su']['mean'])
                if 'cov' in list(df['Su'].keys()):
                    self.txt_Su_c.insert(0,df['Su']['cov'])
                    ii=dist.index(df['Su']['dist'])
                    self.combo_Su.current(ii)
            if ii==4:
                self.txt_Sy_m.insert(0,df['Sy']['mean'])
                if 'cov' in list(df['Sy'].keys()):
                    self.txt_Sy_c.insert(0,df['Sy']['cov'])
                    ii=dist.index(df['Sy']['dist'])
                    self.combo_Sy.current(ii)
            if ii==5:
                self.txt_Lsh_m.insert(0,df['Lsh']['mean'])
                if 'cov' in list(df['Lsh'].keys()):
                    self.txt_Lsh_c.insert(0,df['Lsh']['cov'])
                    ii=dist.index(df['Lsh']['dist'])
                    self.combo_Lsh.current(ii)
            if ii==6:
                self.txt_th_m.insert(0,df['th']['mean'])
                if 'cov' in list(df['th'].keys()):
                    self.txt_th_c.insert(0,df['th']['cov'])
                    ii=dist.index(df['th']['dist'])
                    self.combo_th.current(ii)
            if ii==7:
                self.txt_Limp_m.insert(0,df['Limp']['mean'])
                if 'cov' in list(df['Limp'].keys()):
                    self.txt_Limp_c.insert(0,df['Limp']['cov'])
                    ii=dist.index(df['Limp']['dist'])
                    self.combo_Limp.current(ii)
            if ii==8:
                self.txt_v_m.insert(0,df['v']['mean'])
                if 'cov' in list(df['v'].keys()):
                    self.txt_v_c.insert(0,df['v']['cov'])
                    ii=dist.index(df['v']['dist'])
                    self.combo_v.current(ii)                    
            if ii==13:
                self.txt_Me_m.insert(0,df['Me']['mean'])
                if 'cov' in list(df['Me'].keys()):
                    self.txt_Me_c.insert(0,df['Me']['cov'])
                    ii=dist.index(df['Me']['dist'])
                    self.combo_Me.current(ii)
        for i in range(len(self.formula.const)):
            const=self.formula.const[i]
            ii=self.var.index(const)
            if ii==0:
                self.txt_b_m.insert(0,df['b']['mean'])
            if ii==1:
                self.txt_d_m.insert(0,df['d']['mean'])
            if ii==2:
                self.txt_m_m.insert(0,df['m']['mean'])
            if ii==3:
                self.txt_Su_m.insert(0,df['Su']['mean'])
            if ii==4:
                self.txt_Sy_m.insert(0,df['Sy']['mean'])
            if ii==5:
                self.txt_Lsh_m.insert(0,df['Lsh']['mean'])
            if ii==6:
                self.txt_th_m.insert(0,df['th']['mean'])
            if ii==7:
                self.txt_Limp_m.insert(0,df['Limp']['mean'])
            if ii==8:
                self.txt_v_m.insert(0,df['v']['mean'])
            if ii==9:
                self.txt_ro_imp.insert(0,df['ro_imp']['mean'])
            #if ii==10:
                #self.txt_a10.insert(0,df['a10']['mean'])
            if ii==10:
                self.combo_shape.set(df['shape'])
            if ii==11:
                self.combo_frag.set(df['fragment'])
            if ii==12:
                self.combo_mat.set(df['Material'])
            if ii==13:
                self.txt_Me_m.insert(0,df['Me']['mean'])

    def dfAdd(self,df):
        #画面の入力データから数値を読み取りdf内に組み込む
        #['b', 'd', 'm', 'Su', 'Sy','Lsh', 'th', 'Limp', 'v','Me']
        for i in range(len(self.formula.variable)):
            var=self.formula.variable[i]
            ii=self.var.index(var)
            if ii==0: 
                df['b']={}
                df['b']['mean']=float(self.txt_b_m.get())
                if self.iProb:
                    df['b']['cov']=float(self.txt_b_c.get())
                    df['b']['dist']=self.combo_b.get()
            if ii==1:
                df['d']={} 
                df['d']['mean']=float(self.txt_d_m.get())
                if self.iProb:
                    df['d']['cov']=float(self.txt_d_c.get())
                    df['d']['dist']=self.combo_d.get()
                df['m']={} 
                df['m']['mean']=float(self.txt_m_m.get())
                if self.iProb:
                    df['m']['cov']=float(self.txt_m_c.get())
                    df['m']['dist']=self.combo_m.get()
            if ii==3:
                df['Su']={} 
                df['Su']['mean']=float(self.txt_Su_m.get())
                if self.iProb:
                    df['Su']['cov']=float(self.txt_Su_c.get())
                    df['Su']['dist']=self.combo_Su.get()
            if ii==4:
                df['Sy']={} 
                df['Sy']['mean']=float(self.txt_Sy_m.get())
                if self.iProb:
                    df['Sy']['cov']=float(self.txt_Sy_c.get())
                    df['Sy']['dist']=self.combo_Sy.get()
            if ii==5:
                df['Lsh']={} 
                df['Lsh']['mean']=float(self.txt_Lsh_m.get())
                if self.iProb:
                    df['Lsh']['cov']=float(self.txt_Lsh_c.get())
                    df['Lsh']['dist']=self.combo_Lsh.get()
            if ii==6:
                df['th']={} 
                df['th']['mean']=float(self.txt_th_m.get())
                if self.iProb:
                    df['th']['cov']=float(self.txt_th_c.get())
                    df['th']['dist']=self.combo_th.get()
            if ii==7:
                df['Limp']={} 
                df['Limp']['mean']=float(self.txt_Limp_m.get())
                if self.iProb:
                    df['Limp']['cov']=float(self.txt_Limp_c.get())
                    df['Limp']['dist']=self.combo_Limp.get()
            if ii==8:
                df['v']={} 
                df['v']['mean']=float(self.txt_v_m.get())
                if self.iProb:
                    df['v']['cov']=float(self.txt_v_c.get())
                    df['v']['dist']=self.combo_v.get()
            if ii==13:
                df['Me']={} 
                df['Me']['mean']=float(self.txt_Me_m.get())
                if self.iProb:
                    df['Me']['cov']=float(self.txt_Me_c.get())
                    df['Me']['dist']=self.combo_Me.get()
        return df
    def dfAddC(self,df):
        #['b', 'd', 'm', 'Su', 'Sy','Lsh', 'th', 'Limp', 'v']
        for i in range(len(self.formula.const)):
            const=self.formula.const[i]
            ii=self.var.index(const)
            if ii==0:
                df['b']={} 
                df['b']['mean']=float(self.txt_b_m.get())
            if ii==1:
                df['d']={} 
                df['d']['mean']=float(self.txt_d_m.get())
            if ii==2:
                df['m']={} 
                df['m']['mean']=float(self.txt_m_m.get())
            if ii==3:
                df['Su']={} 
                df['Su']['mean']=float(self.txt_Su_m.get())
            if ii==4:
                df['Sy']={} 
                df['Sy']['mean']=float(self.txt_Sy_m.get())
            if ii==5:
                df['Lsh']={} 
                df['Lsh']['mean']=float(self.txt_Lsh_m.get())
            if ii==6:
                df['th']={} 
                df['th']['mean']=float(self.txt_th_m.get())
            if ii==7:
                df['Limp']={} 
                df['Limp']['mean']=float(self.txt_Limp_m.get())
            if ii==8:
                df['v']={} 
                df['v']['mean']=float(self.txt_v_m.get())
            if ii==9:
                df['ro_imp']={} 
                df['ro_imp']['mean']=float(self.txt_ro_imp.get())
            #if ii==10:
                #df['a10']={} 
                #df['a10']['mean']=float(self.txt_a10.get())
            if ii==10:
                df['shape']={}
                df['shape']=self.combo_shape.get()
            if ii==11:
                df['fragment']={}
                df['fragment']=self.combo_frag.get()
            if ii==12:
                df['Material']={}
                df['Material']=self.combo_mat.get()
            if ii==13:
                df['Me']={} 
                df['Me']['mean']=float(self.txt_Me_m.get())
        return df
    def makeNormal(self):
        self.Clear()
        var=self.formula.variable
        for i in range(len(var)):
            ii=self.var.index(var[i])
            if ii==0:
                self.txt_b_m['state']='normal'
                self.txt_b_c['state']='normal'
                self.combo_b['state']='normal'
            if ii==1:
                self.txt_d_m['state']='normal' 
                self.txt_d_c['state']='normal'
                self.combo_d['state']='normal'
            if ii==2:
                self.txt_m_m['state']='normal' 
                self.txt_m_c['state']='normal'
                self.combo_m['state']='normal'
            if ii==3:
                self.txt_Su_m['state']='normal' 
                self.txt_Su_c['state']='normal'
                self.combo_Su['state']='normal'
            if ii==4:
                self.txt_Sy_m['state']='normal' 
                self.txt_Sy_c['state']='normal'
                self.combo_Sy['state']='normal'
            if ii==5:
                self.txt_Lsh_m['state']='normal' 
                self.txt_Lsh_c['state']='normal'
                self.combo_Lsh['state']='normal'
            if ii==6:
                self.txt_th_m['state']='normal' 
                self.txt_th_c['state']='normal'
                self.combo_th['state']='normal'
            if ii==7:
                self.txt_Limp_m['state']='normal' 
                self.txt_Limp_c['state']='normal'
                self.combo_Limp['state']='normal'
            if ii==8:
                self.txt_v_m['state']='normal'                 
                self.txt_v_c['state']='normal'
                self.combo_v['state']='normal'                    
            if ii==9:
                self.txt_ro_imp['state']='normal'
            #if ii==10:
                #self.txt_a10['state']='normal'
            if ii==10:
                self.combo_shape['state']='normal'
            if ii==11:
                self.combo_frag['state']='normal'
            if ii==12:
                self.combo_mat['state']='normal'
            if ii==13:
                self.txt_Me_m['state']='normal' 
                self.txt_Me_c['state']='normal'
                self.combo_Me['state']='normal'                
                
            

    def makeConst(self):
        const=self.formula.const #適用範囲チェック用の文字列
        self.lbl_b['text']=''
        self.lbl_d['text']=''
        self.lbl_m['text']=''
        self.lbl_Su['text']=''
        self.lbl_Sy['text']=''
        self.lbl_Lsh['text']=''
        self.lbl_th['text']=''
        self.lbl_Limp['text']=''
        self.lbl_v['text']=''
        self.lbl_ro_imp['text']=''
        #self.lbl_a10['text']=''
        self.lbl_shape['text']=''
        self.lbl_frag['text']=''
        self.lbl_Material['text']=''
        self.lbl_Me['text']=''
        for i in range(len(const)):
            self.setAst(self.var.index(const[i]))       
    def setAst(self,i):
        if i==0: self.lbl_b['text']='*'; self.txt_b_m['state']='normal'
        if i==1: self.lbl_d['text']='*'; self.txt_d_m['state']='normal'
        if i==2: self.lbl_m['text']='*'; self.txt_m_m['state']='normal'
        if i==3: self.lbl_Su['text']='*'; self.txt_Su_m['state']='normal'
        if i==4: self.lbl_Sy['text']='*'; self.txt_Sy_m['state']='normal'
        if i==5: self.lbl_Lsh['text']='*'; self.txt_Lsh_m['state']='normal'
        if i==6: self.lbl_th['text']='*'; self.txt_th_m['state']='normal'
        if i==7: self.lbl_Limp['text']='*'; self.txt_Limp_m['state']='normal'
        if i==8: self.lbl_v['text']='*'; self.txt_v_m['state']='normal'
        if i==9: self.lbl_ro_imp['text']='*' ; self.txt_ro_imp['state']='normal'
        #if i==10: self.lbl_a10['text']='*' ; self.txt_a10['state']='normal' 
        if i==10: self.lbl_shape['text']='*' ; self.combo_shape.config(state='normal');self.combo_shape['values']=['flat','hemisperical']
        if i==11: self.lbl_frag['text']='*' ; self.combo_frag.config(state='normal');self.combo_frag['values']=['Standard','Alternative']
        if i==12: self.lbl_Material['text']='*' ; self.combo_mat.config(state='normal'); self.combo_mat['values']=self.formula.MatList()      
    def makeDisable(self):
        #['b', 'd', 'm', 'Su', 'Sy','Lsh', 'th', 'Limp', 'v']
        self.txt_b_m['state']='disable'
        self.txt_b_c['state']='disable'
        self.txt_d_m['state']='disable'
        self.txt_d_c['state']='disable'
        self.txt_m_m['state']='disable'
        self.txt_m_c['state']='disable'
        self.txt_Su_m['state']='disable'
        self.txt_Su_c['state']='disable'
        self.txt_Sy_m['state']='disable'
        self.txt_Sy_c['state']='disable'
        self.txt_Lsh_m['state']='disable'
        self.txt_Lsh_c['state']='disable'
        self.txt_th_m['state']='disable'
        self.txt_th_c['state']='disable'
        self.txt_Limp_m['state']='disable'
        self.txt_Limp_c['state']='disable'
        self.txt_v_m.insert(0,'0')
        self.txt_v_m['state']='disable'
        self.txt_v_c['state']='disable'
        self.txt_Me_m['state']='disable'
        self.txt_Me_c['state']='disable'
        self.txt_ro_imp.insert(0,'10000')
        #self.txt_a10.insert(0,'1750(aluminum),4000(RHA)')
        self.txt_ro_imp['state']='disable'
        #self.txt_a10['state']='disable'
        #self.txt_shape.insert(0,'flat or hemispherical')
        #self.txt_shape['state']='disable'
        self.combo_shape.config(state='disabled')
        #self.txt_frag.insert(0,'Standard or Alternative')
        #self.txt_frag['state']='disable'
        self.combo_frag.config(state='disabled')
        self.combo_mat.config(state='disabled')
        self.combo_b.config(state='disabled')
        self.combo_d.config(state='disabled')
        self.combo_m.config(state='disabled')
        self.combo_Limp.config(state='disabled')
        self.combo_Lsh.config(state='disabled')
        self.combo_v.config(state='disabled')
        self.combo_th.config(state='disabled')
        self.combo_Su.config(state='disabled')
        self.combo_Sy.config(state='disabled')
        self.combo_Me.config(state='disabled')
    def change_out_item(self):
        iOut=self.out_item.get()
 
        if iOut==0:
            print('*** Output is redirected to Panel')
            # 標準出力を一時的にリダイレクトする
            sys.stdout = StringIO() 
        else:
            # 元の標準出力に戻す
            sys.stdout = self.original_stdout
            print('*** Output is redirected to Standard Output')
    def change_anal_item(self):
        self.iProb=self.var_prob.get()
    def change_selected_item(self):
        self.Clear()
        iFormula=self.var_item.get()
        if iFormula==0:
            self.formula=pen.AlyLi()
        if iFormula==1:
            self.formula=pen.BRL()
        if iFormula==2:
            self.formula=pen.DeMarre()
        if iFormula==3:
            self.formula=pen.Jowett()
        if iFormula==4:
            self.formula=pen.Lambert()
        if iFormula==5:
            self.formula=pen.Neilson()
        if iFormula==6:
            self.formula=pen.Ohte()
        if iFormula==7:
            self.formula=pen.SRI()
        if iFormula==8:
            self.formula=pen.SwRI()
        if iFormula==9:
            self.formula=pen.THOR()
        if iFormula==10:
            self.formula=pen.WenJones()
        self.makeDisable() #入力エディタを全てdisableにする
        self.makeNormal() #公式のパラメータの入力エディタを全てenableにする
        self.makeConst()#適用範囲チェック用のパラメータに*をつける
        #self.txt_Text.delete("1.0","end")
        #self.txt_Text.insert(1.0,self.formula.__doc__)
        if self.var_draw.get()==0:
            self.combo_item.config(state='normal')
            self.makeItem()
        else:
            self.combo_item.config(state='disabled')
        self.txt_Text.insert(1.0,self.formula.__doc__)
        return
    def makeItem(self):
        """
        等高線描画項目を構成し、comboboxに入力する
        """
        var=self.formula.variable
        vv=['PoF','Beta']
        for v in var:
            vv.append('ar_'+v)
            self.combo_item['values']=vv
    def transText(self,text):
        self.txt_Text=text
class InterPenet():
    """
    確率論的解析のGUIを管理するクラス
    """
    def __init__(self):
        root = tk.Tk()
        root.geometry('1000x700')
        app = Application(master=root)
        app.master.title('Penetration analysis system')
        app.txt_Text=tk.Text(height=25,width=70)
        xx=150
        app.txt_Text.place(x=150+260+85,y=30)
        app.btn_v.place(x=150,y=366)
        app.btn_p.place(x=150+100,y=366)
        app.change_anal_item()
        app.change_selected_item()
        app.txt_Text.delete("1.0","end")
        app.txt_Text.insert(1.0,"\n  ---  ©2024 Shinsuke Sakai, Ver 1.4  ---\n\n   1.Choose analysis radio button\n         (-Evaluate V_lim- or -Probabilistic analysis-).\n\n   2.Push [Load]button and select input file(***.pkl).\n\n   3.Push [Calc]button.")
        app.transText(app.txt_Text)
        app.button_calc.place(x=xx,y=366+48+48)
        app.change_out_item()
        app.mainloop()
class Drawing():      
    def __init__(self):
        root = tk.Tk()
        en=15
        root.geometry('1000x700')
        app = Application(master=root)
        app.master.title('Drawing system')
        app.btn_p.invoke()
        app.change_selected_item()
        app.label_x=tk.Label(text='X-coord')
        app.label_y=tk.Label(text='Y-coord')
        app.label_min=tk.Label(text='min')
        app.label_max=tk.Label(text='max')
        app.label_div=tk.Label(text='div')
        app.lbl_item=tk.Label(text='item')

        xx=150
        app.btn_contour.place(x=150,y=366)
        app.btn_graph.place(x=150+100,y=366)
        app.button_draw.place(x=xx,y=366+48+48); app.button_calc.place(x=xx-50,y=366+48+48) 
        app.lbl_item.place(x=xx+50,y=366+48+48); app.lbl_item.config(state='disabled')
        app.combo_item.place(x=xx+80,y=366+48+48); app.combo_item.config(state='disabled')
        
        
        app.vv_min=tk.Entry(width=en); app.vv_min.place(x=xx+200,y=366+48+48)
        app.vv_max=tk.Entry(width=en); app.vv_max.place(x=xx+200+100,y=366+48+48)
        app.label_vmin=tk.Label(text='vmin'); app.label_vmin.place(x=xx+200+30,y=366+48+24)
        app.label_vmax=tk.Label(text='vmin'); app.label_vmax.place(x=xx+200+100+30,y=366+48+24)
        app.label_x.place(x=400,y=6)
        app.label_y.place(x=450,y=6)
        app.label_min.place(x=540,y=6)
        app.label_max.place(x=640,y=6)
        app.label_div.place(x=740,y=6)
        for i in range(9):
            btn=tk.Radiobutton(app.master,value=i, variable=app.xcoord_item,command=app.change_contour_item) 
            btn.place(x=400, y=30 + (i * 24))
            bt2=tk.Radiobutton(app.master,value=i, variable=app.ycoord_item,command=app.change_contour_item) 
            bt2.place(x=450, y=30 + (i * 24))
        xx=500; dx=100; yy=30; dy=24
        app.b_min=tk.Entry(width=en)
        app.b_min.place(x=xx,y=yy)
        app.b_max=tk.Entry(width=en)
        app.b_max.place(x=xx+dx,y=yy)
        app.b_div=tk.Entry(width=en)
        app.b_div.place(x=xx+dx*2,y=yy)
        yy+=dy
        app.d_min=tk.Entry(width=en)
        app.d_min.place(x=xx,y=yy)
        app.d_max=tk.Entry(width=en)
        app.d_max.place(x=xx+dx,y=yy)
        app.d_div=tk.Entry(width=en)
        app.d_div.place(x=xx+dx*2,y=yy)        
        yy+=dy
        app.m_min=tk.Entry(width=en)
        app.m_min.place(x=xx,y=yy)
        app.m_max=tk.Entry(width=en)
        app.m_max.place(x=xx+dx,y=yy)
        app.m_div=tk.Entry(width=en)
        app.m_div.place(x=xx+dx*2,y=yy)
        yy+=dy
        app.Su_min=tk.Entry(width=en)
        app.Su_min.place(x=xx,y=yy)
        app.Su_max=tk.Entry(width=en)
        app.Su_max.place(x=xx+dx,y=yy)
        app.Su_div=tk.Entry(width=en)
        app.Su_div.place(x=xx+dx*2,y=yy)
        yy+=dy
        app.Sy_min=tk.Entry(width=en)
        app.Sy_min.place(x=xx,y=yy)
        app.Sy_max=tk.Entry(width=en)
        app.Sy_max.place(x=xx+dx,y=yy)
        app.Sy_div=tk.Entry(width=en)
        app.Sy_div.place(x=xx+dx*2,y=yy)
        yy+=dy
        app.Lsh_min=tk.Entry(width=en)
        app.Lsh_min.place(x=xx,y=yy)
        app.Lsh_max=tk.Entry(width=en)
        app.Lsh_max.place(x=xx+dx,y=yy)
        app.Lsh_div=tk.Entry(width=en)
        app.Lsh_div.place(x=xx+dx*2,y=yy)
        yy+=dy
        app.th_min=tk.Entry(width=en)
        app.th_min.place(x=xx,y=yy)
        app.th_max=tk.Entry(width=en)
        app.th_max.place(x=xx+dx,y=yy)
        app.th_div=tk.Entry(width=en)
        app.th_div.place(x=xx+dx*2,y=yy)
        yy+=dy
        app.Limp_min=tk.Entry(width=en)
        app.Limp_min.place(x=xx,y=yy)
        app.Limp_max=tk.Entry(width=en)
        app.Limp_max.place(x=xx+dx,y=yy)
        app.Limp_div=tk.Entry(width=en)
        app.Limp_div.place(x=xx+dx*2,y=yy)
        yy+=dy
        app.v_min=tk.Entry(width=en)
        app.v_min.place(x=xx,y=yy)
        app.v_max=tk.Entry(width=en)
        app.v_max.place(x=xx+dx,y=yy)
        app.v_div=tk.Entry(width=en)
        app.v_div.place(x=xx+dx*2,y=yy)
        
             
        app.mainloop()
