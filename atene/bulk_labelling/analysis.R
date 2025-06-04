# Load necessary libraries
library(tidyverse)
library(readxl)
library(lme4)
library(emmeans)
library(lmerTest)

# # Load data
# data <- read_excel("/Users/atenejonauskyte/EC_project_Image_analysis/Sau data/grouped_areas_mMEC_lMEC.xlsx") 
# 
# # pivot data to prep it for statistical analysis
# data_longer = data %>% 
#   pivot_longer(col = mMEC_1055:lMEC_1117, names_to = "channel")
# 
# # get two separate columns for EC part and animal ID
# dataframe_animal_channel <- str_split_fixed(data_longer$channel, pattern = "_", n = 2)
# 
# data_longer$ec_subregion <- dataframe_animal_channel[, 1]
# data_longer$animal_id <- dataframe_animal_channel[, 2]
# 
# 
# pattern <- regex("^PFC$|^orbital$|^motor$|^somatosensory$|^anterior cingulate$|^temporal association$|^visual$|^retrosplenial$", ignore_case = TRUE)
# 
# custom_order <- c("PFC", "orbital", "motor", "somatosensory", "anterior cingulate", "temporal association", "visual", "retrosplenial")
# 
# # Filter the dataset to only include the areas in the pattern list
# data_longer <- data_longer %>%
#   filter(str_detect(area, pattern)) %>%
#   mutate(area = factor(area, levels = custom_order)) %>%
#   arrange(area)
# 
# # get sum for each channel of each animal and normalise
# grouped_sum = data_longer %>% 
#   group_by(ec_subregion, animal_id) %>% 
#   summarise(sum=sum(value), .groups = "drop")
# 
# data_normalised <- data_longer %>%
#   left_join(grouped_sum, by = c("ec_subregion", "animal_id")) %>%
#   mutate(normalized_value = value / sum) %>%
#   select(-sum)
# 
# # generate normalised file
# write.csv(data_normalised, "data_normalised.csv", row.names = FALSE)




#read the data file
data_normalised = read_csv("/Users/atenejonauskyte/EC_project_Image_analysis/Sau data/data_normalised.csv")

# set as factors
data_normalised$animal_id <- as.factor(data_normalised$animal_id)
data_normalised$ec_subregion <- as.factor(data_normalised$ec_subregion)
data_normalised$area <- as.factor(data_normalised$area)


# Fit the mixed-effects model with Animal_ID as a random effect
data_lme <- lmer(sqrt(normalized_value) ~ ec_subregion * area  + (1 | animal_id) , data = data_normalised)
anova(data_lme, ddf="Kenward-Roger")
summary(data_lme, ddf="Kenward-Roger")

# check assumptions (seems like a transformation is needed -> used sqrt as it gave best results in )
#plot(data_lme) # residual variance looks better after sqrt transformation
#hist(resid(data_lme))




emmeans_results <- emmeans(data_lme, "ec_subregion", by = "area") # remember that the effect sizes are of the sqrt transformed data
emmeans_results %>% 
  contrast(., method = "pairwise", by = "area") %>% 
  summary(by = NULL, adjust = "holm")

confint(pairs(emmeans_results)) # remember that the effect sizes are of the sqrt transformed data



# get the mean values for ploting preliminary plot
group_means <- data_normalised %>% 
  group_by(area, ec_subregion) %>% 
  summarize(mean = mean(normalized_value))

# plot for visual inspection of normalised values
ggplot(data_normalised, aes(
  x = area,
  y = normalized_value,
)) +
  geom_line(aes(color = ec_subregion,
            group = interaction(animal_id, ec_subregion))) +
  geom_point(aes(shape=ec_subregion, color = ec_subregion)) +
  geom_line(data = group_means, aes(x=area, y=mean, group = ec_subregion, color = ec_subregion), size = 1)

