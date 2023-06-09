from buttons.models import Button, Language


CODES = [
    {
        'name': 'html',
        'code': """
        <!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Document</title>
</head>
<body>
</body>
</html>
        """
    },
    {
        'name': 'css',
        'code': """
.Link-root {
  display: block;
  color: inherit;
}

html {
  scroll-behavior: smooth;
}

@supports ((-webkit-filter: blur()) or (filter: blur())) {
}

img {
  max-width: 100%;
}

.c15 {
  margin-bottom: 25px;
}

.c15,
.c15 td,
.c15 tr {
  border: 1px solid rgb(214, 214, 214);
}

    """
    },
    {
        'name': 'js',
        'code': """
const myPromise = new Promise(function(resolve, reject){
    console.log("Выполнение асинхронной операции");
     
    return "Привет мир!";
});
const x = 4;
const y = 0;
const myPromise = new Promise(function(resolve, reject){
 
    if(y === 0) {
        reject("Переданы некорректные данные");
    }
    else{
        const z = x / y;
        resolve(z);
    }
});
    """
    },
    {
        'name': 'python',
        'code': """
def test(request):
    buttons = Button.objects.all()
    content = {
        'buttons': buttons,
        'style':style,
    }
    return render(request, 'buttons/test.html', content)
    """
    },
    {
        'name': 'php',
        'code': """
<?php
include "welcome.php";
 
$name = "Tom";
welcome($name);
?>
    """
    },
    {
        'name': 'sql',
        'code': """
CREATE TABLE Products
(
    Id SERIAL PRIMARY KEY,
    ProductName VARCHAR(30) NOT NULL,
    Manufacturer VARCHAR(20) NOT NULL,
    ProductCount INTEGER DEFAULT 0,
    Price NUMERIC
);
INSERT INTO Products  (ProductName, Manufacturer, ProductCount, Price)
VALUES
('iPhone X', 'Apple', 2, 71000),
('iPhone 8', 'Apple', 3, 56000),
('Galaxy S9', 'Samsung', 6, 56000),
('Galaxy S8 Plus', 'Samsung', 2, 46000),
('Desire 12', 'HTC', 3, 26000);
    """
    },
]
Button.objects.all().delete()
for item in CODES:
    print(item['name'], '*' * 50)
    Button.objects.create(
        text=item['code'],
        type= Language.objects.get(pk=item['name']),
        name=item['name'],
    )