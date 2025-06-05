from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.scrollview import ScrollView
from kivy.uix.button import Button
import json
import os

class trackerLayout(BoxLayout): #inherits from BoxLayout
    pass
    #Load previous expenses from json if file exists
    def load_expenses(self):
        if os.path.exists("expenses.json"):
            with open("expenses.json","r")as f:
                self.expenses=json.load(f)
        else:
            self.expenses=[]
    
    def add_expense_to_list(self,amount,note):
        from kivy.clock import Clock
        label=Label(
            text=f"{amount:.2f}€ - {note if note else 'No note'}",
            size_hint_y=None,
            height=30,
            halign='left',
            valign='middle'
        )
        label.bind(size=label.setter('text_size')) #Wrap notes
        self.expense_list_layout.add_widget(label)
        
        def scroll_to_bottom(*args):
            self.scroll_view.scroll_y=0
        
        Clock.schedule_once(scroll_to_bottom,0)
            
    #initialization        
    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        self.load_expenses() #update expenses list from json file
        
        #Labels
        amount=self.ids.amount_input.text
        
        note=self.ids.note_input.text

        self.ids.status_label.text="Expense added"        
        
        total=sum(exp[0] for exp in self.expenses) #var total with sum of expenses
        self.ids.sum_label.text=f"Total Expenses:{total:.2f}€"
        
        #DISPLAY OF FULL LIST OF EXPENSES
        self.expense_list_layout = BoxLayout(orientation='vertical',size_hint_y=None)
        self.expense_list_layout.bind(minimum_height=self.expense_list_layout.setter('height'))

        self.scroll_view=ScrollView(size_hint=(1,1))
        self.scroll_view.add_widget(self.expense_list_layout)
        self.add_widget(self.scroll_view)
        
        for amount,note in self.expenses:
            self.add_expense_to_list(amount,note)
        
    def save_expenses(self):
        with open("expenses.json","w") as f:
            json.dump(self.expenses,f)
        
    def add_expense(self,**args):
        amount_text=self.ids.amount_input.text.strip()
        note_text=self.note_input.text.strip()
        
        if not amount_text:
            self.status.text="Please enter an amount."
            return
        try:
            amount=float(amount_text)
            if amount<=0:
                self.status.text="Amount must be greater than 0."
                return
        except ValueError:
            self.status.text="Invalid amount entered."
            return
        
        self.expenses.append((amount,note_text)) #add expense in list
        self.add_expense_to_list(amount,note_text)
        self.ids.status_label.text=f"Added expense: €{amount:.2f} - {note_text if note_text else 'No note'}"
        total=sum(exp[0] for exp in self.expenses)
        self.ids.sum_label.text=f"Total expenses: {total:.2f}€"
        self.save_expenses()
        
        self.amount_input.text=""
        self.note_input.text=""
        
class trackerApp(App):
    def build(self):
        return trackerLayout()

if __name__ == "__main__":
    trackerApp().run()

