def calculer_score(mentor, mentore, disponibilites):
	matieres_communes = set(mentor["points_forts"]) & set(mentore["points_faibles"])	total_besoins = len(mentore["points_faibles"])
if total_besoins > 0 :
		total_besoins = (len(matieres_communes) / total_besoins) * 60
else :
		total_besoins = 0

	dispo_mentor = set(disponibilites.get(mentor["id"] , []))
	dispo_mentore = set(disponibilites.get(mentore["id"] , []))
	creneaux_communs = dispo_mentor & dispo_mentore
	total_creneaux = len(dispo_mentore)

	if total_creneaux > 0:
		score_dispos = (len(creneaux_communs)/ total_creneaux) * 30
	else:
		
		score_dispos = O

	fillieres_proches =  {frozenset({"SI" , "GL"}), {frozenset({"IA" , "IM"})}
	paire = frozenset({mentor["filiere"], mentore["filiere"]})

	if mentor["filiere"] = mentore["filiere"]:
		scrore_filiere = 10
	elif paire in fillieres_proches :
		score_filiere = 6
 	else:
		score_filiere = 0

	return round(min(score_competences + score_dispos + score_filiere, 100.0), 2)


