using Pkg
Pkg.add("Mongoc")

import Mongoc

Mongoc.Client("mongodb+srv://minsurchoi:Minsur2003@cluster0.fbawjgk.mongodb.net/tls=true")
Mongoc.ping(client)
