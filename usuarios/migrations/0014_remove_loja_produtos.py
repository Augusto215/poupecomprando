# Generated by Django 5.0 on 2024-01-20 20:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('usuarios', '0013_valerefeicao_loja_frete_gratis_carrinhoitem_carrinho_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='loja',
            name='produtos',
        ),
    ]
