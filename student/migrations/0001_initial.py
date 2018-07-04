# Generated by Django 2.0.6 on 2018-07-03 11:36

from django.db import migrations, models
import django.db.models.deletion
import student.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('masters', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='AcademicQualificationDetails',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('last_updated', models.DateTimeField(auto_now=True)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('a_level', models.CharField(blank=True, max_length=255, null=True)),
                ('a_level_year', models.CharField(blank=True, max_length=255, null=True)),
                ('a_level_result', models.CharField(blank=True, max_length=255, null=True)),
                ('a_level_result_document', models.FileField(upload_to=student.models.content_file_name_report)),
                ('o_level', models.CharField(blank=True, max_length=255, null=True)),
                ('o_level_year', models.CharField(blank=True, max_length=255, null=True)),
                ('o_level_result', models.CharField(blank=True, max_length=255, null=True)),
                ('o_level_result_document', models.FileField(upload_to=student.models.content_file_name_report)),
                ('high_school', models.CharField(blank=True, max_length=255, null=True)),
                ('high_school_year', models.CharField(blank=True, max_length=255, null=True)),
                ('high_school_result', models.CharField(blank=True, max_length=255, null=True)),
                ('high_school_result_document', models.FileField(upload_to=student.models.content_file_name_report)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ApplicantAboutDetails',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('last_updated', models.DateTimeField(auto_now=True)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('about_yourself', models.CharField(blank=True, max_length=255, null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ApplicantAcademicProgressDetails',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('last_updated', models.DateTimeField(auto_now=True)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('date', models.DateField()),
                ('gpa_scored', models.CharField(blank=True, max_length=255, null=True)),
                ('gpa_from', models.CharField(blank=True, max_length=255, null=True)),
                ('cgpa_scored', models.CharField(blank=True, max_length=255, null=True)),
                ('cgpa_from', models.CharField(blank=True, max_length=255, null=True)),
                ('transcript_document', models.FileField(upload_to=student.models.content_file_name_report)),
                ('semester', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='applicant_progress_semester_rel', to='masters.SemesterDetails')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ApplicantAgreementDetails',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('last_updated', models.DateTimeField(auto_now=True)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('four_parties_agreement_document', models.FileField(upload_to=student.models.content_file_name_report)),
                ('education_loan_agreement_document', models.FileField(upload_to=student.models.content_file_name_report)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ApplicantDevelopmentProgramDetails',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('last_updated', models.DateTimeField(auto_now=True)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('certificate_document', models.FileField(upload_to=student.models.content_file_name_report)),
                ('module', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='development_program_module_rel', to='masters.ModuleDetails')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ApplicantPsychometricTestDetails',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('last_updated', models.DateTimeField(auto_now=True)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('applicant_id', models.CharField(blank=True, max_length=255, null=True)),
                ('result', models.CharField(blank=True, max_length=255, null=True)),
                ('test_result_document', models.FileField(upload_to=student.models.content_file_name_report)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ApplicationDetails',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('last_updated', models.DateTimeField(auto_now=True)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('first_name', models.CharField(max_length=255)),
                ('middle_name', models.CharField(blank=True, max_length=255, null=True)),
                ('last_name', models.CharField(blank=True, max_length=255, null=True)),
                ('birth_date', models.DateField()),
                ('gender', models.CharField(max_length=25)),
                ('religion', models.CharField(blank=True, max_length=255, null=True)),
                ('id_number', models.CharField(blank=True, max_length=100, null=True)),
                ('passport_number', models.CharField(blank=True, max_length=100, null=True)),
                ('passport_issue_country', models.CharField(blank=True, max_length=100, null=True)),
                ('telephone_hp', models.CharField(blank=True, max_length=16, null=True)),
                ('telephone_home', models.CharField(blank=True, max_length=16, null=True)),
                ('email', models.EmailField(blank=True, max_length=255, null=True)),
                ('image', models.FileField(upload_to=student.models.content_file_name_image)),
                ('wife_name', models.CharField(blank=True, max_length=255, null=True)),
                ('wife_income', models.IntegerField(blank=True, null=True)),
                ('wife_pay_slip', models.FileField(upload_to=student.models.content_file_name_report)),
                ('wife_occupation', models.CharField(blank=True, max_length=255, null=True)),
                ('wife_telephone_home', models.CharField(blank=True, max_length=16, null=True)),
                ('wife_dob', models.DateField()),
                ('wife_email', models.EmailField(blank=True, max_length=255, null=True)),
                ('father_name', models.CharField(blank=True, max_length=255, null=True)),
                ('father_income', models.IntegerField(blank=True, null=True)),
                ('father_pay_slip', models.FileField(upload_to=student.models.content_file_name_report)),
                ('father_occupation', models.CharField(blank=True, max_length=255, null=True)),
                ('father_telephone_home', models.CharField(blank=True, max_length=16, null=True)),
                ('father_dob', models.DateField()),
                ('father_email', models.EmailField(blank=True, max_length=255, null=True)),
                ('mother_name', models.CharField(blank=True, max_length=255, null=True)),
                ('mother_income', models.IntegerField(blank=True, null=True)),
                ('mother_pay_slip', models.FileField(upload_to=student.models.content_file_name_report)),
                ('mother_occupation', models.CharField(blank=True, max_length=255, null=True)),
                ('mother_telephone_home', models.CharField(blank=True, max_length=16, null=True)),
                ('mother_dob', models.DateField()),
                ('mother_email', models.EmailField(blank=True, max_length=255, null=True)),
                ('address', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='applicant_address_rel', to='masters.AddressDetails')),
                ('father_nationality', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='father_nationality_rel', to='masters.CountryDetails')),
                ('mother_nationality', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='mother_nationality_rel', to='masters.CountryDetails')),
                ('nationality', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='applicant_nationality_rel', to='masters.CountryDetails')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='CurriculumDetails',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('last_updated', models.DateTimeField(auto_now=True)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('curriculum_name', models.CharField(blank=True, max_length=255, null=True)),
                ('curriculum_year', models.CharField(blank=True, max_length=255, null=True)),
                ('curriculum_result_document', models.FileField(upload_to=student.models.content_file_name_report)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='EnglishQualificationDetails',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('last_updated', models.DateTimeField(auto_now=True)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('english_test_one', models.CharField(blank=True, max_length=255, null=True)),
                ('english_test_one_year', models.CharField(blank=True, max_length=255, null=True)),
                ('english_test_one_result', models.CharField(blank=True, max_length=255, null=True)),
                ('english_test_one_result_document', models.FileField(upload_to=student.models.content_file_name_report)),
                ('english_test_two', models.CharField(blank=True, max_length=255, null=True)),
                ('english_test_two_year', models.CharField(blank=True, max_length=255, null=True)),
                ('english_test_two_result', models.CharField(blank=True, max_length=255, null=True)),
                ('english_test_two_result_document', models.FileField(upload_to=student.models.content_file_name_report)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ExperienceDetails',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('last_updated', models.DateTimeField(auto_now=True)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('work_experience', models.CharField(blank=True, max_length=255, null=True)),
                ('from_date', models.DateField()),
                ('to_date', models.DateField()),
                ('work_experience_document', models.FileField(upload_to=student.models.content_file_name_report)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ScholarshipSelectionDetails',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('last_updated', models.DateTimeField(auto_now=True)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('course_applied', models.CharField(blank=True, max_length=255, null=True)),
                ('admission_letter_document', models.FileField(upload_to=student.models.content_file_name_report)),
                ('scholarship', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='scholarship_selection_rel', to='masters.ScholarshipDetails')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='SiblingDetails',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('last_updated', models.DateTimeField(auto_now=True)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('sibling_name', models.CharField(blank=True, max_length=255, null=True)),
                ('sibling_age', models.IntegerField(blank=True, null=True)),
                ('sibling_status', models.CharField(blank=True, max_length=255, null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='StudentDetails',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('last_updated', models.DateTimeField(auto_now=True)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('first_name', models.CharField(max_length=255)),
                ('middle_name', models.CharField(blank=True, max_length=255, null=True)),
                ('last_name', models.CharField(blank=True, max_length=255, null=True)),
                ('birth_date', models.DateField()),
                ('gender', models.CharField(max_length=25)),
                ('father_name', models.CharField(blank=True, max_length=255, null=True)),
                ('photo', models.FileField(upload_to=student.models.content_file_name_image)),
                ('is_active', models.BooleanField(default=True)),
                ('religion', models.CharField(blank=True, max_length=255, null=True)),
                ('contact_number', models.CharField(blank=True, max_length=16, null=True)),
                ('address', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='student_address_rel', to='masters.AddressDetails')),
                ('nationality', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='student_nationality_rel', to='masters.CountryDetails')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='siblingdetails',
            name='student',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='sibling_applicant_rel', to='student.StudentDetails'),
        ),
        migrations.AddField(
            model_name='scholarshipselectiondetails',
            name='student',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='applicant_scholarship_rel', to='student.StudentDetails'),
        ),
        migrations.AddField(
            model_name='scholarshipselectiondetails',
            name='university',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='university_scholarship_rel', to='masters.UniversityDetails'),
        ),
        migrations.AddField(
            model_name='experiencedetails',
            name='student',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='applicant_experience_rel', to='student.StudentDetails'),
        ),
        migrations.AddField(
            model_name='englishqualificationdetails',
            name='student',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='english_applicant_rel', to='student.StudentDetails'),
        ),
        migrations.AddField(
            model_name='curriculumdetails',
            name='student',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='curriculum_student_rel', to='student.StudentDetails'),
        ),
        migrations.AddField(
            model_name='applicationdetails',
            name='student',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='student_applicant_rel', to='student.StudentDetails'),
        ),
        migrations.AddField(
            model_name='applicationdetails',
            name='wife_nationality',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='wife_nationality_rel', to='masters.CountryDetails'),
        ),
        migrations.AddField(
            model_name='applicantpsychometrictestdetails',
            name='student',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='applicant_psychometric_test_rel', to='student.StudentDetails'),
        ),
        migrations.AddField(
            model_name='applicantdevelopmentprogramdetails',
            name='student',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='development_program_student_rel', to='student.StudentDetails'),
        ),
        migrations.AddField(
            model_name='applicantagreementdetails',
            name='student',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='applicant_agreement_rel', to='student.StudentDetails'),
        ),
        migrations.AddField(
            model_name='applicantacademicprogressdetails',
            name='student',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='applicant_progress_rel', to='student.StudentDetails'),
        ),
        migrations.AddField(
            model_name='applicantacademicprogressdetails',
            name='year',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='applicant_progress_year_rel', to='masters.YearDetails'),
        ),
        migrations.AddField(
            model_name='applicantaboutdetails',
            name='student',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='applicant_about_rel', to='student.StudentDetails'),
        ),
        migrations.AddField(
            model_name='academicqualificationdetails',
            name='student',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='academic_applicant_rel', to='student.StudentDetails'),
        ),
    ]
