import numpy as np
import logging

logging.basicConfig(format="%(asctime)s %(levelname)s %(message)s", level="INFO")

class DecisionMatrix:
    def __init__(self) -> None:
        logging.info("Iniciando a classe da matriz de decisão")

    def normalized_matrix(self, decision_matrix, monotomic_reference_list):
        """
        Function that normalizes the values of the decision matrix (converts them to the same comparable unit, in percentages).

        Args:
            decision_matrix (numpy array): judgment matrix
            monotomic_reference_list (list): list containing '-1' (monotomic cost criterion) or
            '1' (monotomic profit criterion)
        
        Returns:
            norm_matrix (numpy array): normalized matrix with the necessary adjustments
        """
        logging.info("Normalizando os valores da matriz de decisão (descrição em percentuais)")
        aux_matrix = decision_matrix
        for i in range(len(monotomic_reference_list)):
            if monotomic_reference_list[i] == -1:
                aux_matrix[:, i] =  1.0 / aux_matrix[:, i]
        
        sum_lines = np.sum(aux_matrix, axis = 0, dtype='f')
        norm_matriz = aux_matrix / sum_lines
        return norm_matriz
    
    def priority_vector(self, matrix):
        """
        Function that calculates the priority vector of the criteria.

        Args:
            matrix (numpy array): Normalized matrix
        
        Returns:
            vc_vector_norm (numpy array): priority vector calculated from the normalized coefficient of variation
        """
        mean_vector = np.mean(matrix, axis = 1, dtype='f')
        std_vector = (np.std(matrix, axis = 1, dtype = 'f') * np.sqrt(matrix.shape[1]/(matrix.shape[1] - 1)))
        vc_vector = std_vector / mean_vector
        sum_lines = np.sum(vc_vector, axis = 0, dtype = 'f')
        vc_vector_norm = vc_vector / sum_lines
        return vc_vector_norm.reshape((-1,1))

class AHP_GAUSS:
    def __init__(self, decision_matrix, monotomic_reference_list):
        self.decision_matrix = decision_matrix
        self.monotomic_reference_list = monotomic_reference_list
    
    def run_process(self):
        """
        Function that returns the results with the rankings of the choices for the process

        Args:
            None
        
        Returns:
            results (numpy array): results
        """
        class_decision_matrix = DecisionMatrix()
        norm_matrix = class_decision_matrix.normalized_matrix(self.decision_matrix, self.monotomic_reference_list)
        prio_vector = class_decision_matrix.priority_vector(norm_matrix.transpose())
        results = np.dot(norm_matrix, prio_vector)
        return results