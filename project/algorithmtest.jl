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
target_collection_1 = Mongoc.Collection(database, "Cities_Opt_1")
constraints = Mongoc.Collection(database, "Constraints")

function create_trade_dict(doc)
     # Check if "Trade" key exists in the document
    if !haskey(doc, "Trade")
        error("Trade key not found in document: $(doc["Name"])")
    end

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

function quad_opt(imports::Dict{String, Vector{Float64}}, exports::Dict{String, Vector{Float64}})
    
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
        
         w1 = 0.3  # Weight for total imports equals total exports
         w2 = 0.3   # Weight for average of every 10 imports
         w3 = 0.4   # Weight for imports equals exports for each year
        
         
         # Objective function with soft constraints
         @objective(model, Min, 
             sum((adjusted_imports[i] - category_imports[i])^2 + (adjusted_exports[i] - category_exports[i])^2 for i in 1:n) +
             w1 * (sum(adjusted_imports) - sum(adjusted_exports))^2 +
             w2 * sum(max(0, sum(adjusted_imports[i-10:i-1]) - sum(adjusted_imports[i-9:i])) for i in 11:n) +
             w3 * sum((adjusted_exports[i] - adjusted_imports[i])^2 for i in 1:n)
         )

        optimize!(model)
        
        opt_imports[category] = round.(value.(adjusted_imports), digits=2)
        opt_exports[category] = round.(value.(adjusted_exports), digits=2)
    end
    
    return opt_imports, opt_exports
end

Abuja_trade_imports, Abuja_trade_exports = create_trade_dict(Mongoc.find_one(collection, Mongoc.BSON("""{ "Name" : "Abuja" }""")))

opt_imports, opt_exports = quad_opt(Abuja_trade_imports, Abuja_trade_exports)

# Print optimized imports and exports
println("Optimized Imports: ", opt_imports)
println("Optimized Exports: ", opt_exports)