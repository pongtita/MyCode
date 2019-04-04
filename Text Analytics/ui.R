library(shiny)

shinyUI(pageWithSidebar(
  headerPanel("Disney"),
  
  
  
  
  
  sidebarPanel(
    
    
    checkboxInput("outliers",
                  "Show outliers:",
                  T),
    
    selectInput("movie",
                "Choose Movies:",
                list("First Movie" = "First",
                     "Favorite Movie" = "Favorite",
                     "Remake Movie" = "Which_Remake"))
    
),
  




  mainPanel(
    
    tabsetPanel(
    
    tabPanel("Age", plotOutput("diplot")),
      
    tabPanel("Word All", plotOutput("wordall", width = "100%", height = "650px")),  

    tabPanel("Word Cloud", textOutput(""), h3(textOutput("caption")), plotOutput("myplot")),
    
    tabPanel("CorrPlot", plotOutput("ggplot", height = "300px"), plotOutput("ggplot2", height = "300px")),  

    tabPanel("Sentiment", h3(textOutput("sen_fav")), plotOutput("sentiment", height = "700px"))
    )
  )
  
)
)
