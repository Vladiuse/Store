Django, установленный системой автоматической установки cms LTD BEGET
 
=> Действия, описанные ниже, необходимо выполнять в docker-окружении, выполнив команду ниже <=
$ ssh localhost -p222
 
для установки дополнительных модулей используйте pip
сам Django располагается в папке /home/v/vladiuse/test.vim-store.ru/public_html/venv/lib/python3.11/site-packages
 
для начала надо переключиться на текущий virtualenv
заходим в папку с проектом
 
$ cd /home/v/vladiuse/test.vim-store.ru/public_html
$ source venv/bin/activate
 
проверяем, правильно ли определился путь до pip:
$ which pip
/home/v/vladiuse/test.vim-store.ru/public_html/venv/bin/pip
 
теперь мы можем пользоваться pip'ом для установки модулей, не указывая полного пути до исполняемого файла:
 
$ pip install
 
где  имя модуля который мы хотим установить
 
Для перезапуска passenger в папке проекта достаточно выполнить команду touch на пустом файлике restart.txt
 
$ pwd
/home/v/vladiuse/test.vim-store.ru/public_html/HelloDjango/HelloDjango/tmp
$ touch restart.txt