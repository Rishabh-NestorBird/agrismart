Agrismart -- Agriculture Inventory & Farm Management System
Agrismart is a custom application built with the Frappe Framework to
manage farm details, agricultural inventory, stock movements, and
purchase requests.
Overview
The application has four main DocTypes:
- Farm -- stores farm name, location, owner, size, and soil type.
- Inventory Item -- maintains item details, current stock, and
  reorder level.
- Stock Transaction -- records Stock In and Stock Out.
- Purchase Request -- manages requests for inventory items and
  their approval status.
Key Features
- Maintain farm and inventory records.
- Record Stock In and Stock Out transactions.
- Recalculate stock from submitted stock transactions.
- Validate quantities and prevent Stock Out when available stock is
  insufficient.
- Show low-stock alerts when stock reaches or falls below the reorder
  level.
- Validate purchase request quantities and required-by dates.
- Manage purchase requests through Draft → Approved → Ordered.
- Configure role-based access for Farmer and Manager.
- View a Farm-wise Inventory Report with available filters.
Technology Stack
- Frappe Framework -- application framework and DocType-based data
  model
- Python -- server-side business logic and validations
- JavaScript -- client-side form behaviour, where configured
- MariaDB -- database used by the Frappe site
- Git & GitHub -- version control and source hosting
How the DocTypes Work Together
1. Create a Farm record.
2. Create an Inventory Item, such as fertilizer or seeds.
3. Record stock movement in Stock Transaction:
   - Stock In adds quantity.
   - Stock Out subtracts quantity.
4. When more stock is needed, create a Purchase Request and move it
   through the configured workflow.
5. Use the Farm-wise Inventory Report to review transaction records.
Note: Creating or approving a Purchase Request does not itself
increase stock. Stock should be recorded through a Stock Transaction.

Business Rules
- Stock transaction quantity must be greater than zero.
- Stock Out is rejected when available stock is insufficient.
- Stock is recalculated from submitted Stock Transactions.
- A low-stock alert is shown when stock is at or below the reorder
  level.
- Purchase request quantity must be positive.
- The required-by date must not be in the past.
- Purchase Request workflow states are Draft, Approved, and Ordered.
Installation
This app requires a working Frappe Bench environment and an existing
site.
Install on an existing Frappe Bench
cd /path/to/frappe-bench
bench get-app https://github.com/Rishabh-NestorBird/agrismart.git --branch main
bench --site your-site-name install-app agrismart
bench --site your-site-name migrate
Replace your-site-name with your actual Frappe site name.
Start the development server
bench start
Open your Frappe site in a browser, for example http://127.0.0.1:8000
if that is your configured local address.
These steps assume Frappe Bench is already installed and configured.
Compatibility depends on the Frappe version and app dependencies.

Repository
View Agrismart on
GitHub
Future Improvements
Possible future enhancements include supplier management, purchase order
integration, richer inventory analytics, and additional automated tests.
License
This project includes an MIT license. See [`license.txt`](license.txt)
for details.
