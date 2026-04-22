from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Trip',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('destination', models.CharField(max_length=120)),
                ('days', models.PositiveIntegerField()),
                ('mood', models.CharField(choices=[('relax', 'Relax'), ('adventure', 'Adventure'), ('romantic', 'Romantic'), ('family', 'Family'), ('cultural', 'Cultural')], max_length=20)),
                ('group_type', models.CharField(choices=[('solo', 'Solo'), ('friends', 'Friends'), ('couple', 'Couple'), ('family', 'Family')], max_length=20)),
                ('budget', models.PositiveIntegerField(help_text='Budget in INR')),
                ('itinerary', models.TextField()),
                ('weather_info', models.TextField(blank=True)),
                ('estimated_cost', models.CharField(blank=True, max_length=100)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='trips', to=settings.AUTH_USER_MODEL)),
            ],
            options={'ordering': ['-created_at']},
        ),
    ]
