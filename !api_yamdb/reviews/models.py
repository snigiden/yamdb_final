from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()

SCORES = [
    (1, 1),
    (2, 2),
    (3, 3),
    (4, 4),
    (5, 5),
    (6, 6),
    (7, 7),
    (8, 8),
    (9, 9),
    (10, 10)
]


class Category(models.Model):
    name = models.CharField(
        max_length=200,
    )
    slug = models.SlugField(
        max_length=50,
        unique=True,
    )

    class Meta:
        verbose_name = 'Категория'
        ordering = ('name',)

    def __str__(self):
        return self.name


class Genre(models.Model):
    name = models.CharField(
        max_length=200,
    )
    slug = models.SlugField(
        max_length=50,
        unique=True,
    )

    class Meta:
        verbose_name = 'Жанр'
        ordering = ('name',)

    def __str__(self):
        return self.name


class Title(models.Model):
    name = models.CharField(
        max_length=200,
    )
    year = models.PositiveIntegerField()
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        related_name='titles',
    )
    genre = models.ManyToManyField(Genre, through='GenreTitle')
    description = models.CharField(
        max_length=256,
        blank=True,
        null=True,
    )

    class Meta:
        verbose_name = 'Произведение'
        ordering = ('name', '-year',)
        indexes = [
            models.Index(fields=['category', ], name='title_category_idx'),
            models.Index(fields=['-year', ], name='title_year_desc_idx'),
        ]

    def __str__(self):
        return self.name


class GenreTitle(models.Model):
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
    )
    genre = models.ForeignKey(
        Genre,
        on_delete=models.CASCADE,
    )


class Review(models.Model):
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='reviews',
    )
    text = models.TextField()
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reviews',
    )
    score = models.PositiveIntegerField(choices=SCORES)
    pub_date = models.DateTimeField(
        auto_now_add=True,
    )

    class Meta:
        ordering = ('-pub_date', )
        constraints = [
            models.UniqueConstraint(
                fields=['author', 'title'],
                name='unique_review',
            )
        ]
        indexes = [
            models.Index(fields=['score', ], name='review_score_idx'),
            models.Index(
                fields=['-pub_date', ],
                name='review_pub_date_desc_idx'
            ),
            models.Index(fields=['title', ], name='review_title_idx'),
            models.Index(fields=['author', ], name='review_author_idx'),
        ]


class Comment(models.Model):
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='comments',
    )
    text = models.TextField()
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
    )

    class Meta:
        indexes = [
            models.Index(fields=['review', ], name='comment_review_idx'),
            models.Index(fields=['author', ], name='comment_author_idx'),
            models.Index(
                fields=['-pub_date', ],
                name='comment_pub_date_desc_idx'
            ),
        ]
