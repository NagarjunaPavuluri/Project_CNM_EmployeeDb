from flask import Flask, render_template,request
import boto3
import json
import mysql.connector
secretManager = boto3.client('secretsmanager')

secretName = 'employee'
response = secretManager.get_secret_value(SecretId=secretName)

secret = json.loads(response['SecretString'])
print(secret)
username = secret['username']
password = secret['password']
hostName = secret['host']
portNumber = secret['port']
dbname = secret['dbInstanceIdentifier']
print('---------'+username+'--------')
app = Flask(__name__)

try:
    conn = mysql.connector.connect(
    host=hostName,
    port=portNumber,
    database=dbname,
    user=username,
    password=password,
    )
except:
    print('connection error')
print('connected')
cursor = conn.cursor()
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/addEmployee', methods=['GET', 'POST'])
def add_employee():
    if request.method == 'POST':
        name = request.form['name']
        age = request.form['age']
        salary = request.form['salary']
        MobileNumber = request.form['MobileNumber']
        mail = request.form['mail']
        
        sql = "INSERT INTO employee_details (name, age,salary,MobileNumber,email) VALUES (%s, %s, %s,%s, %s)"
        val = (name, age,salary,MobileNumber,mail)
        cursor.execute(sql, val)
        conn.commit()
        #sns
        if(mail!=''):
            topicName='employee'
            sns = boto3.client('sns')
            response = sns.create_topic(Name=topicName)
            topicArn = response['TopicArn']
            Subscription = sns.subscribe(
            TopicArn=topicArn,
            Protocol='email',
            Endpoint=mail
        )
        print('-----------'+mail+'--------')
        
        
        return render_template('addSuccess.html')

    return render_template('add.html')


@app.route('/deleteEmployee', methods=['GET', 'POST'])
def delete_employee():
    
    if request.method == 'POST':
        id = request.form['id']

        cursor = conn.cursor()
        sql = "DELETE FROM employee_details WHERE id = %s"
        val = (id,)
        cursor.execute(sql, val)
        conn.commit()

        message = "Employee deleted successfully"
        return render_template('deleteSuccess.html')

    return render_template('delete.html')
    

@app.route('/displayEmployee')
def display_employee():
    cursor = conn.cursor()
    sql = "SELECT * FROM employee_details"
    cursor.execute(sql)
    employees = cursor.fetchall()

    return render_template('display.html', employees=employees)

if __name__ == '__main__':
    app.run(debug=True)
