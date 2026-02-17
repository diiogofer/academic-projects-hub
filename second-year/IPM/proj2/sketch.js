// Bake-off #2 -- Seleção em Interfaces Densas
// IPM 2023-24, Período 3
// Entrega: até às 23h59, dois dias úteis antes do sexto lab (via Fenix)
// Bake-off: durante os laboratórios da semana de 18 de Março

// p5.js reference: https://p5js.org/reference/

// Database (CHANGE THESE!)
const GROUP_NUMBER        = 14;      // Add your group number here as an integer (e.g., 2, 3)
const RECORD_TO_FIREBASE  = true;  // Set to 'true' to record user results to Firebase

// Pixel density and setup variables (DO NOT CHANGE!)
let PPI, PPCM;
const NUM_OF_TRIALS       = 12;     // The numbers of trials (i.e., target selections) to be completed
let continue_button;
let legendas;                       // The item list from the "legendas" CSV

// Metrics (DO NOT CHANGE!)
let testStartTime, testEndTime;     // time between the start and end of one attempt (8 trials)
let hits 			      = 0;      // number of successful selections
let misses 			      = 0;      // number of missed selections (used to calculate accuracy)
let database;                       // Firebase DB  

// Study control parameters (DO NOT CHANGE!)
let draw_targets          = false;  // used to control what to show in draw()
let trials;                         // contains the order of targets that activate in the test
let current_trial         = 0;      // the current trial number (indexes into trials array above)
let attempt               = 0;      // users complete each test twice to account for practice (attemps 0 and 1)

// Target list and layout variables

// MY VARIABLES
let debug = true;
let target_radius;
let horizontal_margin;
let vertical_margin;
let targets               = [];
let sortedLegendas        = [];
let rows                  = 8;
let columns               = 10;

// NEW VARIABLES
let target_width;
let target_height;

// Ensures important data is loaded before the program starts
function preload()
{
  // id,name,...
  legendas = loadTable('G_'+GROUP_NUMBER+'.csv', 'csv', 'header');
}

// Runs once at the start
function setup()
{
  createCanvas(700, 500);    // window size in px before we go into fullScreen()
  frameRate(60);             // frame rate (DO NOT CHANGE!)
  
  // CODIGO ALTERADO
  sortLegendas();
  if(debug) printSortedLegendas();
  
  randomizeTrials();         // randomize the trial order at the start of execution
  drawUserIDScreen();        // draws the user start-up screen (student ID and display size)
}

// Runs every frame and redraws the screen
function draw()
{
  if (draw_targets && attempt < 2)
  {     
    // The user is interacting with the 6x3 target grid
    background(color(155,155,155));        // sets background to black
    
    // Print trial count at the top left-corner of the canvas
    textFont("Arial", 16);
    fill(color(255,255,255));
    textAlign(LEFT);
    text("Trial " + (current_trial + 1) + " of " + trials.length, 50, 20);
        
    // Draw all targets
    for(let target of targets) {target.draw()}
    
    // Draws the target label to be selected in the current trial. We include 
    // a black rectangle behind the trial label for optimal contrast in case 
    // you change the background colour of the sketch (DO NOT CHANGE THESE!)
    fill(color(0,0,0));
    rect(0, height - 40, width, 40);
 
    textFont("Arial", 20); 
    fill(color(255,255,255)); 
    textAlign(CENTER); 
    text(legendas.getString(trials[current_trial],1), width/2, height - 20);
  }
}

// Print and save results at the end of 12 trials
function printAndSavePerformance()
{
  // DO NOT CHANGE THESE! 
  let accuracy			= parseFloat(hits * 100) / parseFloat(hits + misses);
  let test_time         = (testEndTime - testStartTime) / 1000;
  let time_per_target   = nf((test_time) / parseFloat(hits + misses), 0, 3);
  let penalty           = constrain((((parseFloat(95) - (parseFloat(hits * 100) / parseFloat(hits + misses))) * 0.2)), 0, 100);
  let target_w_penalty	= nf(((test_time) / parseFloat(hits + misses) + penalty), 0, 3);
  let timestamp         = day() + "/" + month() + "/" + year() + "  " + hour() + ":" + minute() + ":" + second();
  
  textFont("Arial", 18);
  background(color(0,0,0));   // clears screen
  fill(color(255,255,255));   // set text fill color to white
  textAlign(LEFT);
  text(timestamp, 10, 20);    // display time on screen (top-left corner)
  
  textAlign(CENTER);
  text("Attempt " + (attempt + 1) + " out of 2 completed!", width/2, 60); 
  text("Hits: " + hits, width/2, 100);
  text("Misses: " + misses, width/2, 120);
  text("Accuracy: " + accuracy + "%", width/2, 140);
  text("Total time taken: " + test_time + "s", width/2, 160);
  text("Average time per target: " + time_per_target + "s", width/2, 180);
  text("Average time for each target (+ penalty): " + target_w_penalty + "s", width/2, 220);

  // Saves results (DO NOT CHANGE!)
  let attempt_data = 
  {
        project_from:       GROUP_NUMBER,
        assessed_by:        student_ID,
        test_completed_by:  timestamp,
        attempt:            attempt,
        hits:               hits,
        misses:             misses,
        accuracy:           accuracy,
        attempt_duration:   test_time,
        time_per_target:    time_per_target,
        target_w_penalty:   target_w_penalty,
  }
  
  // Sends data to DB (DO NOT CHANGE!)
  if (RECORD_TO_FIREBASE)
  {
    // Access the Firebase DB
    if (attempt === 0)
    {
      firebase.initializeApp(firebaseConfig);
      database = firebase.database();
    }
    
    // Adds user performance results
    let db_ref = database.ref('G' + GROUP_NUMBER);
    db_ref.push(attempt_data);
  }
}

// Mouse button was pressed - lets test to see if hit was in the correct target
function mousePressed() 
{
  // Only look for mouse releases during the actual test
  // (i.e., during target selections)
  if (draw_targets)
  {
  for(let target of targets) {
    // Check if the user clicked over one of the targets
        if (target.clicked(mouseX, mouseY)) 
        {
          // Checks if it was the correct target
          if (target.id === trials[current_trial] + 1) hits++;
          else misses++;
        
          current_trial++;              // Move on to the next trial/target
          // Check if the user has completed all trials
          if (current_trial === NUM_OF_TRIALS) {
            testEndTime = millis();
            draw_targets = false;          // Stop showing targets and the user performance results
            printAndSavePerformance();     // Print the user's results on-screen and send these to the DB
            attempt++;                      
      
            // If there's an attempt to go create a button to start this
            if (attempt < 2) {
              continue_button = createButton('START 2ND ATTEMPT');
              continue_button.mouseReleased(continueTest);
              continue_button.position(width/2 - continue_button.size().width/2, height/2 - continue_button.size().height/2);
            }
          }
          // Check if this was the first selection in an attempt
          else if (current_trial === 1) testStartTime = millis(); 
        }      
      }
    }  
  
}

// Evoked after the user starts its second (and last) attempt
function continueTest()
{
  // Re-randomize the trial order
  randomizeTrials();
  
  // Resets performance variables
  hits = 0;
  misses = 0;
  
  current_trial = 0;
  continue_button.remove();
  
  // Shows the targets again
  draw_targets = true; 
}

// Creates and positions the UI targets
function createTargets() {
  targets = [];  // Clear old targets

  let total_target_width = columns * target_width;
  let total_target_height = rows * target_height;

  // Starting position for centered grid
  let startX = width / 2 - total_target_width / 2 + target_width / 2;
  let x = startX;
  let y = height / 2 - total_target_height / 2 + target_height / 2;

  for (let i = 0; i < sortedLegendas.length; i++) {
    let target_id = sortedLegendas[i].ID;
    let target_label = sortedLegendas[i].City;

    if (i % columns === 0 && i !== 0) {
      x = startX;  // New row
      y += target_height;
    }

    let target = new Target(x, y, target_width, target_height, target_label, target_id);
    targets.push(target);

    x += target_width;  // Move to next column
  }
}

// Is invoked when the canvas is resized (e.g., when we go fullscreen)
function windowResized() 
{
  if (fullscreen())
  {
    resizeCanvas(windowWidth, windowHeight);
    
    // DO NOT CHANGE THE NEXT THREE LINES!
    let display        = new Display({ diagonal: display_size }, window.screen);
    PPI                = display.ppi;                      // calculates pixels per inch
    PPCM               = PPI / 2.54;                       // calculates pixels per cm
  
    // Make your decisions in 'cm', so that targets have the same size for all participants
    // Below we find out out white space we can have between 2 cm targets
    let screen_width   = display.width * 2.54;             // screen width
    let screen_height  = display.height * 2.54;            // screen height

    // Creates and positions the UI targets according to the white space defined above (in cm!)
    // 80 represent some margins around the display (e.g., for text)
    //target_radius = 1 * PPCM;
    target_width = 2.4 * PPCM;
    target_height = 2 * PPCM;
    
    createTargets();

    // Starts drawing targets immediately after we go fullscreen
    draw_targets = true;
  }
}

function sortLegendas() {
  sortedLegendas = []; // Reset before sorting
  
  for (let i = 0; i < legendas.getRowCount(); i++) {
    sortedLegendas.push({
      ID: legendas.getNum(i, 0),  
      City: legendas.getString(i, 1),
      Lat: legendas.getNum(i, 2),
      Lng: legendas.getNum(i, 3),
      Country: legendas.getString(i, 4),
      ISO2: legendas.getString(i, 5),
      Population: legendas.getNum(i, 6),
    });
  }

  // Sort by city name
  sortedLegendas.sort((a, b) => a.City.localeCompare(b.City));
}


function printSortedLegendas() {
  let data = [];
  for (let i = 0; i < legendas.getRowCount(); i++) {
    data.push({
      ID: legendas.getString(i, 0),
      City: legendas.getString(i, 1),
      Country: legendas.getString(i, 4),
      Population: legendas.getString(i, 6),
    });
  }
  print(data);
}