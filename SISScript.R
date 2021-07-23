library(tidyverse)
library(ggrepel)
library(magrittr)

dfplaycv <- read_csv("dfPlay5_cv.csv")
total_points <- read_csv("PlayerTotalPoints.csv")
skill_positions <- read_csv("SkillPositionPlayers.csv")
pbp <- read_csv("PlayByPlay.csv")

unique(dfplaycv$CoverageScheme)

Coverages <- c("Cover 0", "Cover 1", "Cover 3", "Cover 2", "Cover 4", "Cover 6", "Man Cover 2", "Tampa 2")

Closed <- c("Cover 1", "Cover 3")

Open <- c("Cover 0", "Cover 2", "Cover 4", "Cover 6", "Man Cover 2", "Tampa 2")

dfplaycv <- dfplaycv %>% 
  filter(CoverageScheme %in% Coverages)
  
dfplaycv <- dfplaycv %>% 
  mutate(MOF = ifelse(CoverageScheme == Closed, "MOFC", "MOFO"))

coverages_cvdata <- dfplaycv %>%
  group_by(concept_cv, CoverageScheme) %>% 
  summarise(EPA_per_Play = mean(EPA),
            EPA_sum = sum(EPA),
            Concept_Count = n())

MOFC_cvdata <- dfplaycv %>% 
  filter(MOF == "MOFC") %>% 
  group_by(concept_cv, MOF) %>% 
  summarise(MOFCEPA_per_Play = mean(EPA),
            MOFCEPA_sum = sum(EPA),
            MOFCConcept_Count = n())

MOFO_cvdata <- dfplaycv %>% 
  filter(MOF == "MOFO") %>% 
  group_by(concept_cv, MOF) %>% 
  summarise(MOFOEPA_per_Play = mean(EPA),
            MOFOEPA_sum = sum(EPA),
            MOFOConcept_Count = n())

MOF_epaavg <- dfplaycv %>% 
  group_by(concept_cv) %>% 
  summarise(EPA_per_Play = mean(EPA))

MOF_cvdata <- MOFC_cvdata %>% 
  inner_join(MOFO_cvdata, by = c("concept_cv")) %>% 
  inner_join(MOF_epaavg, by = c("concept_cv"))

ggplot(data = MOF_cvdata, aes(x = MOFCEPA_per_Play, y = MOFOEPA_per_Play, color = EPA_per_Play)) +
  geom_point(size = 7) +
  geom_text_repel(aes(label = concept_cv), size = 4, color = "black") +
  scale_color_gradient2(low = "#d7191c", mid = "#ffff00", high = "#1a9641",
                        midpoint = 0) +
  labs(y = "EPA/Play vs Middle of Field Open", x = "EPA/Play vs Middle of Field Closed",
       title = "Route Concept EPA/Play vs MOFC & MOFO Coverages",
       color = "EPA/Play") +
  theme_bw() + 
  theme(panel.border = element_blank(),
        # panel.grid.minor = element_blank(),
        # panel.grid.major = element_blank(),
        axis.title = element_text(size = 16),
        axis.text.x = element_text(size = 18, face = "bold", margin = margin(5, 0, 20, 0)),
        axis.text.y = element_text(size = 18, face = "bold", margin = margin(0, 5, 0, 20)),
        plot.title = element_text(size = 24, hjust = 0.5),
        plot.subtitle = element_text(size = 16, hjust = 0.5),
        plot.margin = margin(0.5, 0.5, 0.5, 0.5, "cm"),
        legend.title = element_text(size = 14),
        legend.text = element_text(size = 10),
        legend.key.height = unit(2.3, "cm"))

