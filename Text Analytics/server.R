library(shiny)

library(textreadr)
library(dplyr)
data <- read_document(file = "/Users/pongtit/Desktop/Text_analytic/data.txt")

a <- 44
b <- 8
my_data <- as.data.frame(matrix(nrow=a, ncol=b))

for(z in 1:b){
  for(i in 1:a){
    my_data[i,z]<- data[i*b+z-b]
  }#closing z loop
}#closing i loop


my_df <- my_data[,-1]
colnames(my_df) <- c("Age", "First", "Favorite", "Reason", "Like_Remakes", "Which_Remake", "Expect")

mydf <- data_frame(line = 1:352, text = data)
newdf <- mydf[,-1]

my_df$Age <- parse_number(my_df$Age)

################# start
  
shinyServer(function(input, output){
  
  output$diplot <- renderPlot({
    boxplot(my_df$Age,
            outline = input$outliers)
  })
  

  
  output$wordall <- renderPlot({
    frequencies_all <- newdf %>%
      unnest_tokens(word, text) %>%
      anti_join(stop_words) %>%
      count(word, sort=TRUE)
    
    
    pal <- brewer.pal(8, "Dark2")
    
    frequencies_all %>%
      with(wordcloud(word, n, colors = pal))
    
  })
  
  output$caption <- renderText({
    input$movie
  })
  
  
  output$myplot <- renderPlot({
    my_txt_movie <- my_df[,input$movie]
    mydf_movie <- data_frame(line=1:a, text=my_txt_movie)
    
    frequencies_movie <- mydf_movie %>%
      unnest_tokens(word, text) %>%
      anti_join(stop_words) %>%
      count(word, sort=TRUE)
    

    frequencies_movie %>%
      with(wordcloud(word, n, colors = blues9))
  })
  

  
  output$ggplot <- renderPlot({
    my_fav <- data_frame(line=1:a, text=my_df$Favorite)
    my_rem <- data_frame(line=1:a, text=my_df$Which_Remake)
    my_first <- data_frame(line=1:a, text=my_df$First)
    
    library(tidytext)
    
    tidy_fav <- my_fav %>%
      unnest_tokens(word, text) %>%
      anti_join(stop_words)
    
    tidy_rem <- my_rem %>%
      unnest_tokens(word, text) %>%
      anti_join(stop_words)
    
    tidy_first <- my_first %>%
      unnest_tokens(word, text) %>%
      anti_join(stop_words)
    
    library(tidyr)
    library(stringr)
    frequency <- bind_rows(mutate(tidy_fav, movie ="favorite"),
                           mutate(tidy_rem, movie = "remake"),
                           mutate(tidy_first, movie ="first")
    )%>%#closing bind_rows
      mutate(word=str_extract(word, "[a-z']+")) %>%
      count(movie, word) %>%
      group_by(movie) %>%
      mutate(proportion = n/sum(n))%>%
      select(-n) %>%
      spread(movie, proportion) %>%
      gather(movie, proportion, `favorite`, `remake`)
    
    library(ggplot2)
    library(scales)
    ggplot(frequency, aes(x=proportion, y=`first`, 
                          color = abs(`first`- proportion)))+
      geom_abline(color="blue", lty=2)+
      geom_jitter(alpha=.4, size=2.5, width=0.3, height=0.3)+
      geom_text(aes(label=word), check_overlap = TRUE, vjust=1) +
      scale_x_log10(labels = percent_format())+
      scale_y_log10(labels= percent_format())+
      scale_color_gradientn(colours = topo.colors(10))+
      theme_test() +
      facet_wrap(~movie, ncol=2)+
      theme(legend.position = "none")+
      labs(y= "first", x=NULL)
    
  })
  
  output$ggplot2 <- renderPlot({
    my_frequency <- bind_rows(mutate(tidy_fav, movie ="favorite"),
                              mutate(tidy_rem, movie = "remake")
    )%>%#closing bind_rows
      mutate(word=str_extract(word, "[a-z']+")) %>%
      count(movie, word) %>%
      group_by(movie) %>%
      mutate(proportion = n/sum(n))%>%
      select(-n) %>%
      spread(movie, proportion) %>%
      gather(movie, proportion, `favorite`)
    
    
    library(ggplot2)
    library(scales)
    ggplot(my_frequency, aes(x=proportion, y=`remake`, 
                             color = abs(`remake`- proportion)))+
      geom_abline(color="blue", lty=2)+
      geom_jitter(alpha=.4, size=2.5, width=0.3, height=0.3)+
      geom_text(aes(label=word), check_overlap = TRUE, vjust=1) +
      scale_x_log10(labels = percent_format())+
      scale_y_log10(labels= percent_format())+
      scale_color_gradientn(colours = topo.colors(10))+
      theme_test() +
      facet_wrap(~movie, ncol=2)+
      theme(legend.position = "none")+
      labs(y= "remake", x=NULL)
    
    
    
    
  })
  
  
  output$sen_fav <- renderText({
    "Favorite"
    
  })
  
  
  output$sentiment <- renderPlot({
    my_txt_5 <- my_df$Reason
    mydf_5 <- data_frame(line=1:a, text=my_txt_5)
    
    frequencies_5 <- mydf_5 %>%
      unnest_tokens(word, text) %>%
      anti_join(stop_words) %>%
      count(word, sort=TRUE)
    
    frequencies_5 %>%
      inner_join(get_sentiments("bing")) %>%
      count(word, sentiment, sort=TRUE) %>%
      acast(word ~sentiment, value.var="nn", fill=0) %>%
      comparison.cloud(colors = c("pink", "lightgreen"),
                       max.words=100)
  })
  
  
  
})