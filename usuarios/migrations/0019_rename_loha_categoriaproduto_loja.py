# Generated by Django 5.0 on 2024-01-21 07:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('usuarios', '0018_remove_produto_loja_produto_foto_categoriaproduto'),
    ]

    operations = [
        migrations.RenameField(
            model_name='categoriaproduto',
            old_name='loha',
            new_name='loja',
        ),
    ]
