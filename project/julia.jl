using Pkg
using JuMP
using Ipopt

Pkg.add("Mongoc")
Pkg.add("JuMP")
Pkg.add("Ipopt")

import Mongoc

#Connecting to the mongo database 
client = Mongoc.Client("localhost", 27017)

#Database is named QLAB, Collection is named Cities, documents are named cities 
database = Mongoc.Database(client, "QLAB")
collection = Mongoc.Collection(database, "Cities")

function create_trade_dict(doc)
    #Initialising dicts
    imports = Dict{String, Vector{Float64}}(
        "Animals & Animal Products" => Float64[],
        "Vegetable Products" => Float64[],
        "Animal or Vegetable Fats and Oils and their Cleavage Products; Prepared Edible Fats; Animal or Vegetable Waxes" => Float64[],
        "Prepared Foodstuffs; Beverages, Spirits, Vinegar, Tobacco and Manufactured Tobacco Substitutes" => Float64[],
        "Mineral Products" => Float64[],
        "Products of the Chemical or Allied Industries" => Float64[],
        "Plastics and Articles thereof; Rubber and Articles thereof" => Float64[],
        "Raw Hides and Skins, Leather, Furskins, and Articles thereof; Saddlery and Harness; Travel Goods, Handbags, and Similar Containers; Articles of Animal Gut (Other than Silk-worm Gut)" => Float64[],
        "Wood and Articles of Wood; Wood Charcoal; Cork and Articles of Cork; Manufactures of Straw, of Esparto or of Other Plaiting Materials; Basketware and Wickerwork" => Float64[],
        "Pulp of Wood or of Other Fibrous Cellulosic Material; Recovered (Waste and Scrap) Paper or Paperboard; Paper and Paperboard and Articles thereof" => Float64[],
        "Textiles and Textile Articles" => Float64[],
        "Footwear, Headgear, Umbrellas, Sun Umbrellas, Walking-sticks, Seat-sticks, Whips, Riding-crops, and Parts thereof; Prepared Feathers and Articles Made therewith; Artificial Flowers; Articles of Human Hair" => Float64[],
        "Articles of Stone, Plaster, Cement, Asbestos, Mica or Similar Materials; Ceramic Products; Glass and Glassware" => Float64[],
        "Natural or Cultured Pearls, Precious or Semi-precious Stones, Precious Metals, Metals Clad with Precious Metal, and Articles thereof; Imitation Jewellery; Coin" => Float64[],
        "Base Metals and Articles of Base Metal" => Float64[],
        "Machinery and Mechanical Appliances; Electrical Equipment; Parts thereof; Sound Recorders and Reproducers, Television Image and Sound Recorders and Reproducers, and Parts and Accessories of such Articles" => Float64[],
        "Vehicles, Aircraft, Vessels, and Associated Transport Equipment" => Float64[],
        "Optical, Photographic, Cinematographic, Measuring, Checking, Precision, Medical or Surgical Instruments and Apparatus; Clocks and Watches; Musical Instruments; Parts and Accessories thereof" => Float64[],
        "Arms and Ammunition; Parts and Accessories thereof" => Float64[],
        "Miscellaneous Manufactured Articles" => Float64[],
        "Works of Art, Collectors' Pieces and Antiques" => Float64[]
    )
    
    exports = Dict{String, Vector{Float64}}(
        "Animals & Animal Products" => Float64[],
        "Vegetable Products" => Float64[],
        "Animal or Vegetable Fats and Oils and their Cleavage Products; Prepared Edible Fats; Animal or Vegetable Waxes" => Float64[],
        "Prepared Foodstuffs; Beverages, Spirits, Vinegar, Tobacco and Manufactured Tobacco Substitutes" => Float64[],
        "Mineral Products" => Float64[],
        "Products of the Chemical or Allied Industries" => Float64[],
        "Plastics and Articles thereof; Rubber and Articles thereof" => Float64[],
        "Raw Hides and Skins, Leather, Furskins, and Articles thereof; Saddlery and Harness; Travel Goods, Handbags, and Similar Containers; Articles of Animal Gut (Other than Silk-worm Gut)" => Float64[],
        "Wood and Articles of Wood; Wood Charcoal; Cork and Articles of Cork; Manufactures of Straw, of Esparto or of Other Plaiting Materials; Basketware and Wickerwork" => Float64[],
        "Pulp of Wood or of Other Fibrous Cellulosic Material; Recovered (Waste and Scrap) Paper or Paperboard; Paper and Paperboard and Articles thereof" => Float64[],
        "Textiles and Textile Articles" => Float64[],
        "Footwear, Headgear, Umbrellas, Sun Umbrellas, Walking-sticks, Seat-sticks, Whips, Riding-crops, and Parts thereof; Prepared Feathers and Articles Made therewith; Artificial Flowers; Articles of Human Hair" => Float64[],
        "Articles of Stone, Plaster, Cement, Asbestos, Mica or Similar Materials; Ceramic Products; Glass and Glassware" => Float64[],
        "Natural or Cultured Pearls, Precious or Semi-precious Stones, Precious Metals, Metals Clad with Precious Metal, and Articles thereof; Imitation Jewellery; Coin" => Float64[],
        "Base Metals and Articles of Base Metal" => Float64[],
        "Machinery and Mechanical Appliances; Electrical Equipment; Parts thereof; Sound Recorders and Reproducers, Television Image and Sound Recorders and Reproducers, and Parts and Accessories of such Articles" => Float64[],
        "Vehicles, Aircraft, Vessels, and Associated Transport Equipment" => Float64[],
        "Optical, Photographic, Cinematographic, Measuring, Checking, Precision, Medical or Surgical Instruments and Apparatus; Clocks and Watches; Musical Instruments; Parts and Accessories thereof" => Float64[],
        "Arms and Ammunition; Parts and Accessories thereof" => Float64[],
        "Miscellaneous Manufactured Articles" => Float64[],
        "Works of Art, Collectors' Pieces and Antiques" => Float64[]
    )
    
    for year in 1900:2023
    year_str = string(year)  
        for category in keys(imports)
            push!(imports[category], get(doc["Trade"][year_str]["Imports"], category, 0.0))
            push!(exports[category], get(doc["Trade"][year_str]["Exports"], category, 0.0))
        end
    end

    return imports, exports

end

#Iterate over each document in the collection
#for doc in Mongoc.find(collection)
#Call the function to get imports and exports vectors
#imports, exports = create_trade_dict(doc)
#end

Abuja_trade_imports, Abuja_trade_exports = create_trade_dict(Mongoc.find_one(collection, Mongoc.BSON("""{ "Name" : "Abuja" }""")))
println(Abuja_trade_imports)
println(Abuja_trade_exports)

function optimise_dict(imports::Dict{String, Vector{Float64}}, exports::Dict{String, Vector{Float64}})
    # Ensure the inputs are dictionaries of equal length
    if keys(imports) != keys(exports)
        throw(ArgumentError("The categories in imports and exports must be the same"))
    end
    
    #Create a new dictionary for optimized imports and exports
    opt_imports = Dict{String, Vector{Float64}}()
    opt_exports = Dict{String, Vector{Float64}}()
    
    for category in keys(imports)
        #Get the imports and exports vectors for the current category
        category_imports = imports[category]
        category_exports = exports[category]
        
        #Make sure vectors are of equal length
        if length(category_imports) != length(category_exports)
            throw(ArgumentError("The length of imports and exports vectors for category $category must be equal"))
        end
        
        #Optimize imports and exports using the GLPK model
        n = length(category_imports)
        model = Model(optimizer_with_attributes(Ipopt.Optimizer, "print_level" => 0))
        
        #Variables for adjusted imports and exports
        @variable(model, adjusted_imports[1:n] >= 0)
        @variable(model, adjusted_exports[1:n] >= 0)
        
        #Objective needs checked
        @objective(model, Min, sum((adjusted_imports[i] - category_imports[i])^2 + (adjusted_exports[i] - category_exports[i])^2 for i in 1:n))
        
        #Constraint to make sure total imports equal total exports
        @constraint(model, sum(adjusted_imports) == sum(adjusted_exports))
        
        #Average of every 10 imports should be higher than the last 10 imports
        for i in 11:n
            @constraint(model, sum(adjusted_imports[i-9:i]) / 10 >= sum(adjusted_imports[i-10:i-1]) / 10)
        end
        
        #Constraint to make sure imports total exports after optimisation
        for i in 1:n
            @constraint(model, adjusted_exports[i] == adjusted_imports[i])
        end
        
        optimize!(model)
        
        # Retrieve the optimal values
        opt_imports[category] = value.(adjusted_imports)
        opt_exports[category] = value.(adjusted_exports)
    end
    
    return opt_imports, opt_exports
end

opt_imports, opt_exports = optimise_dict(Abuja_trade_imports, Abuja_trade_exports)

for category in keys(opt_imports)
    println("Optimized Imports for $category: ", opt_imports[category])
    println("Optimized Exports for $category: ", opt_exports[category])
end




