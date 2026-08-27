
import tkinter as tk
from tkinter import messagebox
import random
from itertools import combinations

SUITS=["♠","♥","♦","♣"]
RANKS=["2","3","4","5","6","7","8","9","10","J","Q","K","A"]
VALUES={r:i+2 for i,r in enumerate(RANKS)}
HAND_NAMES=["High Card","One Pair","Two Pair","Three of a Kind","Straight",
            "Flush","Full House","Four of a Kind","Straight Flush"]

def deck():
    d=[(r,s) for s in SUITS for r in RANKS]
    random.shuffle(d); return d

def evaluate5(cards):
    vals=sorted([VALUES[r] for r,s in cards],reverse=True)
    cnt={v:vals.count(v) for v in set(vals)}
    uniq=sorted(set(vals),reverse=True)
    if 14 in uniq: uniq.append(1)
    straight=None
    for i in range(len(uniq)-4):
        if uniq[i]-uniq[i+4]==4:
            straight=uniq[i]; break
    flush=len({s for r,s in cards})==1
    groups=sorted(((n,v) for v,n in cnt.items()),reverse=True)
    quads=[v for n,v in groups if n==4]
    trips=sorted([v for n,v in groups if n==3],reverse=True)
    pairs=sorted([v for n,v in groups if n==2],reverse=True)
    if flush and straight: return (8,straight)
    if quads:
        q=quads[0]; return (7,q,max(v for v in vals if v!=q))
    if trips and pairs: return (6,trips[0],pairs[0])
    if flush: return (5,*vals)
    if straight: return (4,straight)
    if trips:
        t=trips[0]; return (3,t,*sorted([v for v in vals if v!=t],reverse=True))
    if len(pairs)>=2:
        a,b=pairs[:2]; k=max(v for v in vals if v not in (a,b))
        return (2,a,b,k)
    if len(pairs)==1:
        p=pairs[0]; return (1,p,*sorted([v for v in vals if v!=p],reverse=True))
    return (0,*vals)

def best(cards):
    return max(evaluate5(c) for c in combinations(cards,5))

class App:
    def __init__(self,root):
        self.root=root
        root.title("Poker Lab — Hold'em Practice")
        root.geometry("1120x760")
        root.configure(bg="#0b3524")
        self.points=1000
        self.round=0
        self.build()
        self.new_round()

    def build(self):
        header=tk.Frame(self.root,bg="#071f15",height=62); header.pack(fill="x")
        tk.Label(header,text="POKER LAB",font=("Segoe UI",24,"bold"),
                 fg="white",bg="#071f15").pack(side="left",padx=20,pady=10)
        self.score=tk.Label(header,text="",font=("Segoe UI",13,"bold"),
                            fg="#d9f7df",bg="#071f15")
        self.score.pack(side="right",padx=20)

        self.table=tk.Frame(self.root,bg="#0b3524"); self.table.pack(fill="both",expand=True)
        self.bot_area=tk.Frame(self.table,bg="#0b3524"); self.bot_area.pack(pady=10)
        self.bot_widgets=[]
        for i,name in enumerate(["Bot Alpha","Bot Beta","Bot Gamma"]):
            box=tk.Frame(self.bot_area,bg="#164b32",bd=2,relief="ridge",width=240,height=120)
            box.pack(side="left",padx=12); box.pack_propagate(False)
            lab=tk.Label(box,text=name,font=("Segoe UI",12,"bold"),fg="white",bg="#164b32")
            lab.pack(pady=5)
            cards=tk.Frame(box,bg="#164b32"); cards.pack()
            self.bot_widgets.append((box,cards))

        tk.Label(self.table,text="COMMUNITY CARDS",font=("Segoe UI",10,"bold"),
                 fg="#bfe8ca",bg="#0b3524").pack(pady=(12,4))
        self.board=tk.Frame(self.table,bg="#0b3524"); self.board.pack()

        self.message=tk.Label(self.table,text="",font=("Segoe UI",14,"bold"),
                              fg="white",bg="#0b3524",wraplength=1000)
        self.message.pack(pady=12)

        tk.Label(self.table,text="YOUR HIDDEN HAND",font=("Segoe UI",10,"bold"),
                 fg="#bfe8ca",bg="#0b3524").pack()
        self.hand=tk.Frame(self.table,bg="#0b3524"); self.hand.pack(pady=5)

        controls=tk.Frame(self.table,bg="#0b3524"); controls.pack(pady=12)
        tk.Label(controls,text="Practice-point wheel:",fg="white",bg="#0b3524",
                 font=("Segoe UI",11)).pack(side="left",padx=6)
        self.slider=tk.Scale(controls,from_=10,to=200,resolution=10,orient="horizontal",
                            length=260,showvalue=True,bg="#0b3524",fg="white",
                            highlightthickness=0)
        self.slider.set(50); self.slider.pack(side="left")
        tk.Button(controls,text="Check",command=self.check,font=("Segoe UI",11,"bold"),
                  width=11).pack(side="left",padx=5)
        tk.Button(controls,text="Fold Practice",command=self.fold,font=("Segoe UI",11,"bold"),
                  width=13).pack(side="left",padx=5)
        tk.Button(controls,text="New Round",command=self.new_round,font=("Segoe UI",11,"bold"),
                  width=12).pack(side="left",padx=5)

        tk.Label(self.table,text="The wheel changes practice points only — there is no wagering or cash value.",
                 fg="#a9d7b6",bg="#0b3524",font=("Segoe UI",9)).pack(pady=5)

    def card(self,parent,c=None,hidden=False):
        text="🂠" if hidden else f"{c[0]}{c[1]}"
        fg="#b71c1c" if c and c[1] in "♥♦" else "#111"
        return tk.Label(parent,text=text,width=5,height=2,font=("Segoe UI",18,"bold"),
                        bg="white",fg=fg,relief="raised",bd=2)

    def clear(self,frame):
        for x in frame.winfo_children(): x.destroy()

    def render(self,reveal=False):
        self.score.config(text=f"Practice Points: {self.points}   |   Round: {self.round}")
        self.clear(self.board); self.clear(self.hand)
        for c in self.community:
            self.card(self.board,c).pack(side="left",padx=5)
        for c in self.player:
            self.card(self.hand,c).pack(side="left",padx=5)
        for i,(box,area) in enumerate(self.bot_widgets):
            self.clear(area)
            for c in self.bots[i]:
                self.card(area,c,not reveal).pack(side="left",padx=3)

    def animate_points(self,delta):
        start=self.points
        target=start+delta
        steps=12
        def step(n=0):
            if n>steps:
                self.points=target; self.score.config(text=f"Practice Points: {self.points}   |   Round: {self.round}")
                return
            self.points=round(start+(target-start)*n/steps)
            self.score.config(text=f"Practice Points: {self.points}   |   Round: {self.round}")
            self.root.after(35,lambda:step(n+1))
        step()

    def new_round(self):
        self.round+=1
        d=deck()
        self.player=[d.pop(),d.pop()]
        self.bots=[[d.pop(),d.pop()] for _ in range(3)]
        self.community=[d.pop(),d.pop(),d.pop(),d.pop(),d.pop()]
        self.stage=0
        self.revealed=3
        self.finished=False
        self.render()
        self.message.config(text="Flop is ready. Study your hidden cards and choose Check or Fold Practice.")

    def check(self):
        if self.finished:return
        gain=int(self.slider.get())
        # Reveal the next street as a learning exercise.
        if self.revealed<5:
            self.revealed+=1
            self.render()
            names=["Flop","Turn","River"]
            self.message.config(text=f"{names[self.revealed-3]} revealed. What do you think your best hand is?")
        else:
            self.showdown(gain)

    def fold(self):
        if self.finished:return
        self.finished=True
        self.animate_points(-int(self.slider.get()/2))
        self.message.config(text="Practice fold recorded. Start a new round to try another hand.")
        self.render()

    def showdown(self,gain):
        self.finished=True
        active=self.community
        ph=best(self.player+active)
        results=[best(b+active) for b in self.bots]
        winner=max([("You",ph)]+[(f"Bot {i+1}",h) for i,h in enumerate(results)],key=lambda x:x[1])
        self.render(reveal=True)
        if winner[0]=="You":
            self.animate_points(gain)
            msg=f"You win the practice round! Your hand: {HAND_NAMES[ph[0]]}. +{gain} practice points."
        else:
            self.animate_points(-int(gain/2))
            msg=f"{winner[0]} wins the practice round. Your hand: {HAND_NAMES[ph[0]]}. Practice points -{int(gain/2)}."
        self.message.config(text=msg)

if __name__=="__main__":
    root=tk.Tk()
    App(root)
    root.mainloop()
