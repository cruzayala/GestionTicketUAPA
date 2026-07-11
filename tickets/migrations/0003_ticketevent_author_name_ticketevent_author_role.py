from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tickets', '0002_create_support_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='ticketevent',
            name='author_name',
            field=models.CharField(default='Sistema', max_length=120),
        ),
        migrations.AddField(
            model_name='ticketevent',
            name='author_role',
            field=models.CharField(default='Sistema', max_length=30),
        ),
    ]
