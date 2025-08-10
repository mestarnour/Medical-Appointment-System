class PatientModel :
   def __init__(self, db):
      self.db = db

   def get_all_patients(self):
      query = """
      MATCH (p:Patient)
      RETURN p.id as id, p.name AS name, p.age AS age , p.sexe as sexe
      ORDER BY p.name
      """
      return self.db.query(query)

   def get_patient_by_id(self, patient_id):
      query = "MATCH (p:Patient {id: $patient_id}) RETURN p.name as name, p.age as age,p.id as patient_id ,p.sexe as sexe "
      parameters = {'patient_id': patient_id}
      result = self.db.query(query, parameters)
      print(result)  # Debugging
      if result:
         return result[0]  # Assurez-vous de retourner le bon patient
      return None



   def create_patient(self,name,age,sexe,id):
         query="""
         CREATE (p:Patient {id:$id,name:$name,age:$age,sexe:$sexe})

"""
         parameters={
            "id":id,
            "name":name,
            "age":age,
            "sexe":sexe
         }
         self.db.query(query,parameters)
   def nombre_reservations(self ,id):
         query="""
         MATCH (p:Patient {id: $id})-[:A_PRIS]->(r:RendezVous)
         RETURN count(r) AS total_reservations
"""
         result=self.db.query(query,{"id":id})
         return result[0]['total_reservations'] if result else 0
   
   def add_pathology_to_patient(self, patient_id, pathology_id):
    query = """
    MATCH (p:Patient {id: $patient_id}), (pa:Pathologie {id: $pathology_id})
    CREATE (p)-[:DIAGNOSTIQUE_AVEC]->(pa)
    RETURN p.name AS patient_name, pa.name AS pathology_name
    """
    parameters = {'patient_id': patient_id, 'pathology_id': pathology_id}
    result = self.db.query(query, parameters)
    if result:
        return result[0]  # Retourne les noms des entités ajoutées pour la confirmation
    return None