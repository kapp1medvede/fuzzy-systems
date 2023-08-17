using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using FuzzyLogicController.FLC;
using FuzzyLogicController.MFs;
using FuzzyLogicController.RuleEngine;
using FuzzyLogicController;
public class FuzzyConroller : MonoBehaviour
{ 
    private float speed = 4;
    private Vector3 targetPosition;
    private bool isMoving = false;
    private bool sensor = false; 
    Vector3 v;
    Vector3 worldPosition;
    // Start is called before the first frame update
    void Start()
    { 

    }
 

    // Update is called once per frame
 
    
    void Update ( ) 
    {
        List<float> sensors=sensorOn(); 
        if (Input.GetMouseButtonDown(0))
        {
            RaycastHit hit;
            Ray ray = Camera.main.ScreenPointToRay(Input.mousePosition);
            if (Physics.Raycast(ray, out hit))
               targetPosition =  hit.point;
               targetPosition.y = transform.position.y; 
               isMoving = true;
        }
        if ( isMoving ) { 

            transform.position = Vector3.MoveTowards(transform.position, targetPosition, 4 * Time.deltaTime);

            transform.LookAt(targetPosition, Vector3.up);
           
                List<double> s = Initializate(sensors[0], sensors[1], sensors[2], sensors[3]); 
             
                transform.Translate((float)s[0]*0.01f  , 0, (float)s[1] * 0.001f); 
         

                if (Vector3.Distance(transform.position, targetPosition) < 0.5f)
                isMoving = false;
        } 
    }

    List<double> Initializate(double left, double right, double front, double back)
    {
        Config conf = new Config(ImpMethod.Prod,ConnMethod.Min);

        LingVariable leftSensor = new LingVariable("leftSensor", VarType.Input);
        leftSensor.setRange(0, 1000);
        leftSensor.addMF(new Trapmf("close", 0, 15, 30, 45));
        leftSensor.addMF(new Trimf("normal", 30, 50, 75));
        leftSensor.addMF(new Trapmf("far", 60, 75, 90, 1000));

        LingVariable rightSensor = new LingVariable("rightSensor", VarType.Input);
        rightSensor.setRange(0, 1000);
        rightSensor.addMF(new Trapmf("close", 0, 15, 30, 45));
        rightSensor.addMF(new Trimf("normal", 30, 50, 75));
        rightSensor.addMF(new Trapmf("far", 60, 75, 90, 1000));

        LingVariable frontSensor = new LingVariable("frontSensor", VarType.Input);
        frontSensor.setRange(0, 1000);
        frontSensor.addMF(new Trapmf("close", 0, 15, 30, 45));
        frontSensor.addMF(new Trimf("normal", 30, 50, 75));
        frontSensor.addMF(new Trapmf("far", 60, 75, 90, 1000));

        LingVariable backSensor = new LingVariable("backSensor", VarType.Input);
        backSensor.setRange(0, 1000);
        backSensor.addMF(new Trapmf("close", 0, 15, 30, 45));
        backSensor.addMF(new Trimf("normal", 30, 50, 75));
        backSensor.addMF(new Trapmf("far", 60, 75, 90, 1000));


        LingVariable leftRight = new LingVariable("leftRight", VarType.Output);
        leftRight.setRange(-15, 15);
        leftRight.addMF(new Trapmf("left", -15, -10, -2, 0));
        leftRight.addMF(new Trapmf("right", -2, 0, 10, 15)); 

        LingVariable Motor = new LingVariable("Motor", VarType.Output);
        Motor.setRange(-105, 105);
        Motor.addMF(new Trimf("fast_back", -105, -80, -60));
        Motor.addMF(new Trimf("normal_back", -75, -50, -30));
        Motor.addMF(new Trimf("low_back", -45, -20, -5));
        Motor.addMF(new Trimf("stop", -10, 0, 10));
        Motor.addMF(new Trimf("low_front", 5, 20, 45));
        Motor.addMF(new Trimf("normal_front", 30, 50, 75));
        Motor.addMF(new Trimf("fast_front", 60, 80, 105));

        FLC c = new FLC(conf); 
        FuzzySet set1 = new FuzzySet(c.Fuzzification(left, leftSensor), leftSensor.Name);
        FuzzySet set2 = new FuzzySet(c.Fuzzification(right, rightSensor), rightSensor.Name);
        FuzzySet set3 = new FuzzySet(c.Fuzzification(front, frontSensor), frontSensor.Name);
        FuzzySet set4 = new FuzzySet(c.Fuzzification(back, backSensor), backSensor.Name); 


        List<FuzzySet> fuzset = new List<FuzzySet>();
        fuzset.Add(set1);
        fuzset.Add(set2);
        fuzset.Add(set3);
        fuzset.Add(set4);
 

        List<RuleItem> rule1in = new List<RuleItem>(); 
        List<RuleItem> rule2in = new List<RuleItem>();
        List<RuleItem> rule3in = new List<RuleItem>();
        List<RuleItem> rule4in = new List<RuleItem>();
        List<RuleItem> rule5in = new List<RuleItem>();
        List<RuleItem> rule6in = new List<RuleItem>();
        List<RuleItem> rule7in = new List<RuleItem>();
        List<RuleItem> rule8in = new List<RuleItem>();
        List<RuleItem> rule9in = new List<RuleItem>();
        List<RuleItem> rule10in = new List<RuleItem>();
        List<RuleItem> rule11in = new List<RuleItem>();
        List<RuleItem> rule12in = new List<RuleItem>(); 


        rule1in.AddRange(new RuleItem[2] { new RuleItem("leftSensor", "far"), new RuleItem("frontSensor", "close") });
        rule2in.AddRange(new RuleItem[2] { new RuleItem("leftRight", "left"), new RuleItem("Motor", "low_front") });

        rule3in.AddRange(new RuleItem[2] { new RuleItem("rightSensor", "far"), new RuleItem("frontSensor", "close") });
        rule4in.AddRange(new RuleItem[2] { new RuleItem("leftRight", "right"), new RuleItem("Motor", "low_front") });

        rule5in.AddRange(new RuleItem[2] { new RuleItem("leftSensor", "close"), new RuleItem("frontSensor", "far") });
        rule6in.AddRange(new RuleItem[2] { new RuleItem("leftRight", "right"), new RuleItem("Motor", "low_front") });

        rule7in.AddRange(new RuleItem[2] { new RuleItem("rightSensor", "close"), new RuleItem("frontSensor", "far") });
        rule8in.AddRange(new RuleItem[2] { new RuleItem("leftRight", "left"), new RuleItem("Motor", "low_front") });

        rule9in.AddRange(new RuleItem[2] { new RuleItem("frontSensor", "far"), new RuleItem("rightSensor", "far") });
        rule10in.AddRange(new RuleItem[2] { new RuleItem("leftRight", "right"), new RuleItem("Motor", "fast_front") });

        rule11in.AddRange(new RuleItem[2] { new RuleItem("frontSensor", "far"), new RuleItem("leftSensor", "far") });
        rule12in.AddRange(new RuleItem[2] { new RuleItem("leftRight", "left"), new RuleItem("Motor", "fast_front") });
  
        

        List<Rule> rules = new List<Rule>();
        rules.Add(new Rule(rule1in, rule2in, Connector.And));
        rules.Add(new Rule(rule3in, rule4in, Connector.And));
        rules.Add(new Rule(rule5in, rule6in, Connector.And));
        rules.Add(new Rule(rule7in, rule8in, Connector.And));
        rules.Add(new Rule(rule9in, rule10in, Connector.And));
        rules.Add(new Rule(rule11in, rule12in, Connector.And));
         
        InferEngine engine = new InferEngine(conf, rules, fuzset);

        List<FuzzySet> impli = engine.evaluateRules();
     
        double dir = c.DeFuzzification(impli, leftRight);
        double speed = c.DeFuzzification(impli, Motor); 
        List<double> output= new List<double>();
        output.Add(dir);
        output.Add(speed); 
         
        print("Output Y: " + output[0] + "Output Y1: " + output[1]); 
        return output;
    }

    List<float> sensorOn()
    {
        bool isSensorOn = false;
        float left = 900;
        float right = 900;
        float front= 900;
        float back = 900;
        Vector3 sensor = transform.position;
        float frontSensorAngle = 90;
        float sensorLength = 5;
        RaycastHit hit;
        if (Physics.Raycast(sensor, transform.forward, out hit, sensorLength) && hit.transform.tag != "Terrain")
        {
            Debug.DrawLine(sensor, hit.point);
            isSensorOn = true;
            front = Vector3.Distance(transform.position, hit.point);
        }
        else if (Physics.Raycast(sensor, Quaternion.AngleAxis(30, transform.up) * transform.forward, out hit, sensorLength) && hit.transform.tag != "Terrain")
        {
            Debug.DrawLine(sensor, hit.point);
            isSensorOn = true;
            right = Vector3.Distance(transform.position, hit.point);
        }
        else if (Physics.Raycast(sensor, Quaternion.AngleAxis(-30, transform.up) * transform.forward, out hit, sensorLength) && hit.transform.tag != "Terrain")
        {
            Debug.DrawLine(sensor, hit.point);
            isSensorOn = true;
            left = Vector3.Distance(transform.position, hit.point);
        }  

        List<float> dir = new List<float>();
        dir.Add(left);
        dir.Add(right);
        dir.Add(front);
        dir.Add(back);
        return dir;
    }
}