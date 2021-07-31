@echo off
@echo Lookups...
python manage.py loaddata categories
python manage.py loaddata genres
python manage.py loaddata publishers
python manage.py loaddata reduced_reasons
python manage.py loaddata stock_states
@echo Product Lines...
python manage.py loaddata product_lines
@echo Sub Product Lines...
python manage.py loaddata sub_product_lines
call load_products.bat