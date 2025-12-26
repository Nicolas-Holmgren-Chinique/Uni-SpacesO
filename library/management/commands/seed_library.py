from django.core.management.base import BaseCommand
from library.models import Subject, Textbook

class Command(BaseCommand):
    help = 'Seeds the library with popular free OpenStax textbooks'

    def handle(self, *args, **kwargs):
        self.stdout.write('Seeding library with OpenStax books...')

        # Define subjects and their books
        data = {
            'Mathematics': [
                {
                    'title': 'Calculus Volume 1',
                    'author': 'Edwin "Jed" Herman, Gilbert Strang',
                    'url': 'https://openstax.org/details/books/calculus-volume-1',
                    'cover': 'https://assets.openstax.org/oscms-prodcms/media/documents/Calculus_Volume_1_-_Web_Version_Cover.png',
                    'desc': 'Calculus Volume 1 is designed for the typical two- or three-semester general calculus course, incorporating innovative features to enhance student learning.'
                },
                {
                    'title': 'Algebra and Trigonometry',
                    'author': 'Jay Abramson',
                    'url': 'https://openstax.org/details/books/algebra-and-trigonometry-2e',
                    'cover': 'https://assets.openstax.org/oscms-prodcms/media/documents/Algebra_and_Trigonometry_2e_-_Web_Version_Cover.png',
                    'desc': 'Algebra and Trigonometry 2e provides a comprehensive exploration of algebraic principles and meets scope and sequence requirements for a typical introductory algebra and trigonometry course.'
                }
            ],
            'Physics': [
                {
                    'title': 'University Physics Volume 1',
                    'author': 'Samuel J. Ling, Jeff Sanny, William Moebs',
                    'url': 'https://openstax.org/details/books/university-physics-volume-1',
                    'cover': 'https://assets.openstax.org/oscms-prodcms/media/documents/University_Physics_Volume_1_-_Web_Version_Cover.png',
                    'desc': 'University Physics is a three-volume collection that meets the scope and sequence requirements for two- and three-semester calculus-based physics courses.'
                }
            ],
            'Computer Science': [
                {
                    'title': 'Introduction to Python Programming',
                    'author': 'OpenStax',
                    'url': 'https://openstax.org/details/books/introduction-python-programming',
                    'cover': 'https://assets.openstax.org/oscms-prodcms/media/documents/Introduction_to_Python_Programming_-_Web_Version_Cover.png',
                    'desc': 'Introduction to Python Programming is designed for students with no prior programming experience.'
                }
            ],
            'Psychology': [
                {
                    'title': 'Psychology 2e',
                    'author': 'Rose M. Spielman, William J. Jenkins, Marilyn D. Lovett',
                    'url': 'https://openstax.org/details/books/psychology-2e',
                    'cover': 'https://assets.openstax.org/oscms-prodcms/media/documents/Psychology_2e_-_Web_Version_Cover.png',
                    'desc': 'Psychology 2e is designed to meet scope and sequence requirements for the single-semester introduction to psychology course.'
                }
            ],
            'History': [
                {
                    'title': 'U.S. History',
                    'author': 'P. Scott Corbett, Volker Janssen, John M. Lund',
                    'url': 'https://openstax.org/details/books/us-history',
                    'cover': 'https://assets.openstax.org/oscms-prodcms/media/documents/US_History_-_Web_Version_Cover.png',
                    'desc': 'U.S. History covers the breadth of the chronological history of the United States and also provides the necessary depth to ensure the course is manageable for instructors and students alike.'
                }
            ],
            'Biology': [
                {
                    'title': 'Biology 2e',
                    'author': 'Mary Ann Clark, Matthew Douglas, Jung Choi',
                    'url': 'https://openstax.org/details/books/biology-2e',
                    'cover': 'https://assets.openstax.org/oscms-prodcms/media/documents/Biology_2e_-_Web_Version_Cover.png',
                    'desc': 'Biology 2e is designed to cover the scope and sequence requirements of a typical two-semester biology course for science majors.'
                },
                {
                    'title': 'Concepts of Biology',
                    'author': 'Samantha Fowler, Rebecca Roush, James Wise',
                    'url': 'https://openstax.org/details/books/concepts-biology',
                    'cover': 'https://assets.openstax.org/oscms-prodcms/media/documents/Concepts_of_Biology_-_Web_Version_Cover.png',
                    'desc': 'Concepts of Biology is designed for the typical introductory biology course for nonmajors, covering standard scope and sequence requirements.'
                }
            ],
            'Chemistry': [
                {
                    'title': 'Chemistry 2e',
                    'author': 'Paul Flowers, Klaus Theopold, Richard Langley',
                    'url': 'https://openstax.org/details/books/chemistry-2e',
                    'cover': 'https://assets.openstax.org/oscms-prodcms/media/documents/Chemistry_2e_-_Web_Version_Cover.png',
                    'desc': 'Chemistry 2e is designed to meet the scope and sequence requirements of the two-semester general chemistry course.'
                }
            ],
            'Economics': [
                {
                    'title': 'Principles of Economics 3e',
                    'author': 'David Shapiro, Daniel MacDonald, Steven A. Greenlaw',
                    'url': 'https://openstax.org/details/books/principles-economics-3e',
                    'cover': 'https://assets.openstax.org/oscms-prodcms/media/documents/Principles_of_Economics_3e_-_Web_Version_Cover.png',
                    'desc': 'Principles of Economics 3e covers the scope and sequence of most introductory economics courses.'
                }
            ],
            'Business': [
                {
                    'title': 'Introduction to Business',
                    'author': 'Lawrence J. Gitman, Carl McDaniel, Amit Shah',
                    'url': 'https://openstax.org/details/books/introduction-business',
                    'cover': 'https://assets.openstax.org/oscms-prodcms/media/documents/Introduction_to_Business_-_Web_Version_Cover.png',
                    'desc': 'Introduction to Business covers the scope and sequence of most introductory business courses.'
                }
            ]
        }

        for subject_name, books in data.items():
            subject, _ = Subject.objects.get_or_create(
                name=subject_name, 
                defaults={'slug': subject_name.lower().replace(' ', '-')}
            )
            
            for book_data in books:
                book, created = Textbook.objects.get_or_create(
                    title=book_data['title'],
                    defaults={
                        'author': book_data['author'],
                        'subject': subject,
                        'description': book_data['desc'],
                        'open_access_url': book_data['url'],
                        'cover_image_url': book_data['cover'],
                        'provider': 'OpenStax'
                    }
                )
                if created:
                    self.stdout.write(self.style.SUCCESS(f'Added "{book.title}"'))
                else:
                    self.stdout.write(f'Skipped "{book.title}" (already exists)')

        self.stdout.write(self.style.SUCCESS('Library seeding complete!'))
