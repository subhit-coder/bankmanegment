import streamlit as st
import json
import random
import string
from pathlib import Path

class Bank:
    database = 'database.json'
    data = []

    try:
        if Path(database).exists():
            with open(database) as fs:
                data = json.loads(fs.read())
        else:
            st.warning("⚠️ Database file not found, starting fresh...")
    except Exception as err:
        st.error(f"❌ Error: {err}")

    @classmethod
    def __update(cls):
        with open(cls.database, 'w') as fs:
            fs.write(json.dumps(cls.data, indent=4))

    @staticmethod
    def __accountno():
        alpha = random.choices(string.ascii_letters, k=5)
        digits = random.choices(string.digits, k=4)
        acc_id = alpha + digits
        random.shuffle(acc_id)
        return "".join(acc_id)

    def create_account(self, name, email, phone, pin):
        d = {
            "name": name,
            "email": email,
            "phone no.": phone,
            "pin": pin,
            "Account no.": Bank.__accountno(),
            "Balance": 0
        }
        if len(str(pin)) != 4:
            st.error("❌ PIN must be 4 digits!")
            return
        elif len(str(phone)) != 10:
            st.error("❌ Phone number must be 10 digits!")
            return
        else:
            Bank.data.append(d)
            Bank.__update()
            st.success(f"✅ Account created! Your Account No: {d['Account no.']}")

    def deposit_money(self, accNo, pin, amount):
        user_data = [i for i in Bank.data if i['Account no.'] == accNo and i['pin'] == pin]
        if not user_data:
            st.error("❌ User not found")
        else:
            if amount <= 0:
                st.error("❌ Invalid amount")
            elif amount > 10000:
                st.warning("⚠️ Deposit limit is 10,000")
            else:
                user_data[0]['Balance'] += amount
                Bank.__update()
                st.success("💰 Amount credited successfully!")

    def withdraw_money(self, accNo, pin, amount):
        user_data = [i for i in Bank.data if i['Account no.'] == accNo and i['pin'] == pin]
        if not user_data:
            st.error("❌ User not found")
        else:
            if amount <= 0:
                st.error("❌ Invalid amount")
            elif amount > user_data[0]['Balance']:
                st.error("❌ Insufficient balance")
            elif amount > 10000:
                st.warning("⚠️ Withdrawal limit is 10,000")
            else:
                user_data[0]['Balance'] -= amount
                Bank.__update()
                st.success("💸 Amount debited successfully!")

    def details(self, accNo, pin):
        user_data = [i for i in Bank.data if i['Account no.'] == accNo and i['pin'] == pin]
        if not user_data:
            st.error("❌ User not found")
        else:
            st.json(user_data[0])

    def delete_account(self, accNo, pin):
        user_data = [i for i in Bank.data if i['Account no.'] == accNo and i['pin'] == pin]
        if not user_data:
            st.error("❌ User not found")
        else:
            Bank.data = [i for i in Bank.data if not (i["Account no."] == accNo and i["pin"] == pin)]
            Bank.__update()
            st.success("🗑️ Account deleted successfully!")


# ---------------- STREAMLIT UI ----------------
st.title("🏦 Bank Management System")
st.sidebar.title("📌 Menu")

menu = st.sidebar.radio("Choose an option:", 
                        ["Create Account", "Deposit Money", "Withdraw Money", "Account Details", "Delete Account"])

bank = Bank()

if menu == "Create Account":
    st.subheader("🆕 Create Account")
    name = st.text_input("Enter your name")
    email = st.text_input("Enter your email")
    phone = st.text_input("Enter your phone number")
    pin = st.text_input("Enter your 4-digit PIN", type="password")
    if st.button("Create Account"):
        if name and email and phone and pin:
            bank.create_account(name, email, int(phone), int(pin))
        else:
            st.error("❌ Please fill all fields")

elif menu == "Deposit Money":
    st.subheader("💰 Deposit Money")
    accNo = st.text_input("Enter Account No")
    pin = st.text_input("Enter PIN", type="password")
    amount = st.number_input("Enter amount", min_value=1)
    if st.button("Deposit"):
        bank.deposit_money(accNo, int(pin), amount)

elif menu == "Withdraw Money":
    st.subheader("💸 Withdraw Money")
    accNo = st.text_input("Enter Account No")
    pin = st.text_input("Enter PIN", type="password")
    amount = st.number_input("Enter amount", min_value=1)
    if st.button("Withdraw"):
        bank.withdraw_money(accNo, int(pin), amount)

elif menu == "Account Details":
    st.subheader("📋 Account Details")
    accNo = st.text_input("Enter Account No")
    pin = st.text_input("Enter PIN", type="password")
    if st.button("Show Details"):
        bank.details(accNo, int(pin))

elif menu == "Delete Account":
    st.subheader("🗑️ Delete Account")
    accNo = st.text_input("Enter Account No")
    pin = st.text_input("Enter PIN", type="password")
    if st.button("Delete"):
        bank.delete_account(accNo, int(pin))