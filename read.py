from models import Quote, Author

# Функція для пошуку цитат за тегом
def search_by_tag(tag):
    quotes = Quote.objects(tags=tag)
    print(f"Quotes for tag {tag}:")
    for quote in quotes:
        print(f"- {quote.quote}")
    print()


# Функція для пошуку цитат за ім'ям автора
def search_by_author(author_fullname):
    a = Author.objects(fullname=author_fullname).first()
    if a:
        quotes = Quote.objects(author=a)
        print(f"Quotes of author {author_fullname}:")
        for quote in quotes:
            print(f"- {quote.quote}")
    else:
        print(f"Author {author_fullname} is not known")
    print()


# Функція для пошуку цитат за набором тегів
def search_by_tags(tags):
    tag_list = tags.split(',')
    quotes = Quote.objects(tags__in=tag_list)
    print(f"Quotes for tags {tags}:")
    for quote in quotes:
        print(f"- {quote.quote}")
    print()


if __name__ == '__main__':

    while True:
        request = input("Input (for example: name:Steve Martin, tag:life, tags:life,live, exit): ")
        r = request.split(":")
        if r[0] == 'name':
            author = r[1].strip()
            search_by_author(author)
        elif r[0] == 'tag':
            tag = r[1].strip()
            search_by_tag(tag)
        elif r[0] == 'tags':
            tags = r[1].strip()
            search_by_tags(tags)
        elif r[0] == 'exit':
            break
        else:
            print("Unknown request. Try again")


