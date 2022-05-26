# Generated by Django 4.0.4 on 2022-05-26 12:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='serveurs',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom', models.CharField(max_length=100)),
                ('processeurs', models.IntegerField()),
                ('memoire', models.IntegerField()),
                ('stockage', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='type_de_serveurs',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(max_length=100)),
                ('description', models.TextField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='utilisateurs',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom', models.CharField(max_length=100)),
                ('prenom', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=254, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='services',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom_service', models.CharField(max_length=100)),
                ('date_de_lancement', models.DateField(max_length=100)),
                ('espace_memoire_utilise', models.IntegerField()),
                ('memoire_vive_necessaire', models.IntegerField()),
                ('serveur_de_lancement', models.ForeignKey(null='true', on_delete=django.db.models.deletion.CASCADE, to='adminserver.serveurs')),
            ],
        ),
        migrations.AddField(
            model_name='serveurs',
            name='type_de_serveur',
            field=models.ForeignKey(null='true', on_delete=django.db.models.deletion.CASCADE, to='adminserver.type_de_serveurs'),
        ),
        migrations.CreateModel(
            name='applications',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom_application', models.CharField(max_length=100)),
                ('logo', models.ImageField(upload_to='images')),
                ('serveurs', models.ForeignKey(null='true', on_delete=django.db.models.deletion.CASCADE, to='adminserver.serveurs')),
                ('utilisateurs', models.ForeignKey(null='true', on_delete=django.db.models.deletion.CASCADE, to='adminserver.utilisateurs')),
            ],
        ),
    ]
