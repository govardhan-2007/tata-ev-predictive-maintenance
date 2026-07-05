class MaintenanceAdvisor:

    def get_recommendation(self, prediction):

        recommendations = {

            "Healthy": {
                "action": "Continue normal operation",
                "priority": "Low",
                "inspection": "Routine inspection after 5000 km"
            },

            "Motor Fault": {
                "action": "Inspect motor cooling system",
                "priority": "Critical",
                "inspection": "Check inverter, cooling fan and winding temperature"
            },

            "Battery Fault": {
                "action": "Inspect battery pack",
                "priority": "High",
                "inspection": "Check cell voltage and balancing"
            },

            "Brake Fault": {
                "action": "Inspect braking system",
                "priority": "High",
                "inspection": "Check brake pads and brake temperature"
            },

            "Bearing Fault": {
                "action": "Inspect motor bearings",
                "priority": "Medium",
                "inspection": "Check lubrication and vibration"
            },

            "Tyre Fault": {
                "action": "Inspect tyres",
                "priority": "Medium",
                "inspection": "Check pressure and wheel alignment"
            }
        }

        return recommendations.get(
            prediction,
            recommendations["Healthy"]
        )