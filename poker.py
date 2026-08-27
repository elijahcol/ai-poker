
import tkinter as tk
from tkinter import messagebox
import random

SUITS = ["♠", "♥", "♦", "♣"]
RANKS = ["2","3","4","5","6","7","8","9","10","J","Q","K","A"]
VALUES = {r:i+2 for i,r in enumerate(RANKS)}

def make_deck():
    return [(r,s) for s in SUITS for r in RANKS]

def card_text(c):
    return f"{c[0]}{c[1]}"

def evaluate5(cards):
    vals = sorted([VALUES[r] for r,s in cards], reverse=True)
    counts = {v: vals.count(v) for v in set(vals)}
    unique = sorted(set(vals), reverse=True)
    if 14 in unique:
        unique.append(1)
    straight_high = None
    for i in range(len(unique)-4):
        if unique[i] - unique[i+4] == 4:
            straight_high = unique[i]
            break
    flush = len({s for r,s in cards}) == 1
    if flush and straight_high: return (8, straight_high)
    groups = sorted(((n,v) for v,n in counts.items()), reverse=True)
    quads = [v for n,v in groups if n == 4]
    trips = sorted([v for n,v in groups if n == 3], reverse=True)
    pairs = sorted([v for n,v in groups if n == 2], reverse=True)
    if quads:
        q=quads[0]; return (7,q,max(v for v in vals if v!=q))
    if trips and pairs:
        return (6,trips[0],pairs[0])
    if flush: return (5,*vals)
    if straight_high: return (4,straight_high)
    if trips:
        t=trips[0]; return (3,t,*sorted([v for v in vals if v!=t],reverse=True))
    if len(pairs)>=2:
        p1,p2=pairs[:2]; k=max(v for v in vals if v not in (p1,p2))
        return (2,p1,p2,k)
    if len(pairs)==1:
        p=pairs[0]; return (1,p,*sorted([v for v in vals if v!=p],reverse=True))
    return (0,*vals)

def best_hand(cards):
    from itertools import combinations
    return max(evaluate5(c) for c in combinations(cards,5))

NAMES=["High Card","Pair","Two Pair","Three of a Kind","Straight",
       "Flush","Full House","Four of a Kind","Straight Flush"]

class PokerApp:
    def __init__(self, root):
        self.root=root
        root.title("Windows Poker")
        root.geometry("1000x680")
        root.minsize(850,600)
        self.deck=[]; self.player=[]; self.cpu=[]; self.community=[]
        self.player_chips=1000; self.cpu_chips=1000
        self.pot=0; self.stage="Pre-flop"; self.bet=50
        self.in_hand=False
        self.build()
        self.new_hand()

    def build(self):
        self.root.configure(bg="#123b27")
        top=tk.Frame(self.root,bg="#0d2b1c",height=55); top.pack(fill="x")
        tk.Label(top,text="WINDOWS POKER",font=("Segoe UI",22,"bold"),
                 fg="white",bg="#0d2b1c").pack(side="left",padx=18,pady=10)
        self.info=tk.Label(top,text="",font=("Segoe UI",12),fg="#e8f5e9",bg="#0d2b1c")
        self.info.pack(side="right",padx=18)

        self.cpu_label=tk.Label(self.root,text="",font=("Segoe UI",14,"bold"),
                                fg="white",bg="#123b27")
        self.cpu_label.pack(pady=(14,4))
        self.cpu_cards=tk.Frame(self.root,bg="#123b27"); self.cpu_cards.pack()

        tk.Label(self.root,text="COMMUNITY CARDS",font=("Segoe UI",10,"bold"),
                 fg="#b9e6c5",bg="#123b27").pack(pady=(15,3))
        self.board=tk.Frame(self.root,bg="#123b27"); self.board.pack()

        tk.Label(self.root,text="YOUR CARDS",font=("Segoe UI",10,"bold"),
                 fg="#b9e6c5",bg="#123b27").pack(pady=(15,3))
        self.player_cards=tk.Frame(self.root,bg="#123b27"); self.player_cards.pack()

        self.status=tk.Label(self.root,text="",font=("Segoe UI",14,"bold"),
                             fg="white",bg="#123b27",wraplength=900)
        self.status.pack(pady=15)

        controls=tk.Frame(self.root,bg="#123b27"); controls.pack()
        for txt,cmd in [("Fold",self.fold),("Check",self.check),
                        ("Bet 50",self.bet_action),("New Hand",self.new_hand)]:
            tk.Button(controls,text=txt,command=cmd,font=("Segoe UI",11,"bold"),
                      width=12,padx=6,pady=7).pack(side="left",padx=5)

    def draw_card(self, parent, card=None, hidden=False):
        text="🂠" if hidden else card_text(card)
        fg="#b71c1c" if card and card[1] in "♥♦" else "#111111"
        return tk.Label(parent,text=text,width=5,height=3,font=("Segoe UI",18,"bold"),
                        bg="white",fg=fg,relief="raised",bd=2)

    def refresh(self, reveal=False):
        for f in (self.cpu_cards,self.board,self.player_cards):
            for w in f.winfo_children(): w.destroy()
        for c in self.cpu:
            self.draw_card(self.cpu_cards,c,reveal).pack(side="left",padx=4)
        for c in self.community:
            self.draw_card(self.board,c).pack(side="left",padx=4)
        for c in self.player:
            self.draw_card(self.player_cards,c).pack(side="left",padx=4)
        self.cpu_label.config(text=f"Computer • Chips: {self.cpu_chips}")
        self.info.config(text=f"You: {self.player_chips}   Pot: {self.pot}   Stage: {self.stage}")

    def new_hand(self):
        if self.player_chips <= 0 or self.cpu_chips <= 0:
            self.player_chips=self.cpu_chips=1000
        self.deck=make_deck(); random.shuffle(self.deck)
        self.player=[self.deck.pop(),self.deck.pop()]
        self.cpu=[self.deck.pop(),self.deck.pop()]
        self.community=[]
        self.pot=100
        self.player_chips-=50; self.cpu_chips-=50
        self.stage="Pre-flop"; self.in_hand=True
        self.status.config(text="Your turn — Check, Bet, or Fold.")
        self.refresh()

    def deal_next(self):
        if self.stage=="Pre-flop":
            self.community += [self.deck.pop(),self.deck.pop(),self.deck.pop()]
            self.stage="Flop"
        elif self.stage=="Flop":
            self.community.append(self.deck.pop()); self.stage="Turn"
        elif self.stage=="Turn":
            self.community.append(self.deck.pop()); self.stage="River"
        else:
            self.showdown(); return
        self.refresh()

    def cpu_move(self):
        strength=best_hand(self.cpu+self.community) if len(self.community)>=3 else (0,)
        # Simple play-money AI: folds rarely and bets based on hand category.
        if strength[0] <= 1 and random.random() < .12:
            self.fold(who="Computer"); return
        if self.cpu_chips>=50 and (strength[0]>=2 or random.random()<.25):
            self.cpu_chips-=50; self.pot+=50
        self.deal_next()

    def check(self):
        if not self.in_hand: return
        self.cpu_move()

    def bet_action(self):
        if not self.in_hand: return
        if self.player_chips<50:
            messagebox.showinfo("No chips","You don't have enough chips for a 50-chip bet.")
            return
        self.player_chips-=50; self.pot+=50
        self.cpu_move()

    def fold(self,who="You"):
        if not self.in_hand: return
        self.in_hand=False
        if who=="You":
            self.cpu_chips+=self.pot
            self.status.config(text=f"You folded. Computer wins {self.pot} chips.")
        else:
            self.player_chips+=self.pot
            self.status.config(text=f"Computer folded. You win {self.pot} chips!")
        self.refresh()

    def showdown(self):
        self.in_hand=False
        ph=best_hand(self.player+self.community)
        ch=best_hand(self.cpu+self.community)
        self.refresh(reveal=True)
        if ph>ch:
            self.player_chips+=self.pot
            msg=f"You win {self.pot} chips! {NAMES[ph[0]]} beats {NAMES[ch[0]]}."
        elif ch>ph:
            self.cpu_chips+=self.pot
            msg=f"Computer wins {self.pot} chips. {NAMES[ch[0]]} beats {NAMES[ph[0]]}."
        else:
            self.player_chips+=self.pot//2
            self.cpu_chips+=self.pot-self.pot//2
            msg=f"Split pot. Both have {NAMES[ph[0]]}."
        self.status.config(text=msg)

if __name__=="__main__":
    root=tk.Tk()
    PokerApp(root)
    root.mainloop()
