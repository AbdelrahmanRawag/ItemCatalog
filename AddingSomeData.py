from sqlalchemy import create_engine, asc
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Category, CategoryItem, User

engine = create_engine('sqlite:///database.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

User1 = User(name="Rawag", email="abdelrahmanrawaj@gmail.com",
             picture='https://scontent.fcai3-1.fna.fbcdn.net/v/t1.0-9/23472730_1586239558089651_5567458259598829223_n.jpg?oh=9a62bd0b19b143462f639899059ded12&oe=5B067529')
session.add(User1)
session.commit()

category = Category(name="FootBall")
session.add(category)
session.commit()

item = CategoryItem(name="Ball",
                    description="A ball is a round object (usually spherical but sometimes ovoid) with various uses."
                                " It is used in ball games, where the play of the game follows the state of the ball as it is hit,"
                                " kicked or thrown by players. Balls can also be used for simpler activities,"
                                " such as catch, marbles and juggling", category_id=category.id, user_id=User1.id);
session.add(item)
session.commit()

item = CategoryItem(name="T-shirt",
                    description="A T-shirt (or t shirt, or tee) is a style of unisex fabric shirt named after the T shape of its body and sleeves."
                                " It normally has short sleeves and a round neckline, known as a crew neck,"
                                " which lacks a collar.", category_id=category.id, user_id=User1.id);
session.add(item)
session.commit()

category = Category(name="Rowing")
session.add(category)
session.commit()

item = CategoryItem(name="Boat",
                    description="A boat is a watercraft of a large range of sizes designed to float, plane, work or travel on water."
                                " Small boats are typically found on inland waterways (e.g. rivers and lakes) or in protected coastal areas."
                                " Another definition is a vessel that can be lifted out of the water.",
                    category_id=category.id, user_id=User1.id);
session.add(item)
session.commit()

item = CategoryItem(name="Watch",
                    description="Computer Definition. A rugged, water-resistant wristwatch that includes features such as an alarm, stopwatch,"
                                " compass, heart rate monitor, tachymeter (rotating bezel for calculating speed),"
                                " thermometer and tide indicator (for divers).", category_id=category.id,
                    user_id=User1.id);
session.add(item)
session.commit()

category = Category(name="HandBall")
session.add(category)
session.commit()

item = CategoryItem(name="Ball",
                    description="A ball is a round object (usually spherical but sometimes ovoid) with various uses."
                                " It is used in ball games, where the play of the game follows the state of the ball as it is hit,"
                                " kicked or thrown by players. Balls can also be used for simpler activities, such as catch,"
                                " marbles and juggling.", category_id=category.id, user_id=User1.id);

session.add(item)
session.commit()

item = CategoryItem(name="Ball",
                    description="On some shoes, the heel of the sole has a rubber plate for durability and traction,"
                                " while the front is leather for style. ... The heel is the bottom rear part of a shoe."
                                " Its function is to support the heel of the foot."
                                " They are often made of the same material as the sole of the shoe.",
                    category_id=category.id, user_id=User1.id);
session.add(item)
session.commit()

category = Category(name="Boxing")
session.add(category)
session.commit()

item = CategoryItem(name="Gloves",
                    description="On some shoes, the heel of the sole has a rubber plate for durability and traction,"
                                " while the front is leather for style. ... The heel is the bottom rear part of a shoe."
                                " Its function is to support the heel of the foot."
                                " They are often made of the same material as the sole of the shoe.",
                    category_id=category.id, user_id=User1.id);
session.add(item)
session.commit()

item = CategoryItem(name="Helmet",
                    description="A helmet is a form of protective gear worn to protect the head from injuries."
                                " More specifically, a helmet aids the skull in protecting the human brain. "
                                "Ceremonial or symbolic helmets (e.g. UK policeman's helmet)"
                                " without protective function are sometimes used.", category_id=category.id,
                    user_id=User1.id);
session.add(item)
session.commit()

category = Category(name="Tennis")
session.add(category)
session.commit()

item = CategoryItem(name="Ball",
                    description="A ball is a round object (usually spherical but sometimes ovoid) with various uses."
                                " It is used in ball games, where the play of the game follows the state of the ball as it is hit,"
                                " kicked or thrown by players. Balls can also be used for simpler activities, such as catch,"
                                " marbles and juggling.", category_id=category.id, user_id=User1.id);
session.add(item)
session.commit()

item = CategoryItem(name="Paddle",
                    description="Padel is a racquet sport. In the US and Canada the sport is known as Paddle."
                                " Padel is not to be confused with Platform Tennis, a winter and summer sport typically played at country clubs in the US and Canada,"
                                " with courts heated from below to eliminate snow and water.", category_id=category.id,
                    user_id=User1.id);
session.add(item)
session.commit()

category = Category(name="Swimming")
session.add(category)
session.commit()

item = CategoryItem(name="Glasses",
                    description="Goggles, or safety glasses, are forms of protective eyewear that usually enclose or protect the area surrounding the eye in order to prevent particulates,"
                                " water or chemicals from striking the eyes. They are used in chemistry laboratories and in woodworking."
                                " They are often used in snow sports as well, and in swimming.",
                    category_id=category.id, user_id=User1.id);
session.add(item)
session.commit()

item = CategoryItem(name="Suit",
                    description="A one-piece swimsuit most commonly refers to swimwear worn by women and girls when swimming in the sea or in a swimming pool,"
                                " or for any activity in the sun, such as sun bathing. Today, the one-piece swimsuit is usually a skin-tight garment that covers a female's torso,"
                                " except maybe the back or upper chest.", category_id=category.id, user_id=User1.id);
session.add(item)
session.commit()
